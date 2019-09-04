import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.InputSplit;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.FileSystem;

import java.io.IOException;

import java.util.ArrayList;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

public class CompressedRecordReader extends RecordReader<LongWritable, Text> {
    private LongWritable keyOffset = new LongWritable();
    private Text valueDocument = new Text();
    private ArrayList<Integer> documentSizes = new ArrayList<>();
    private long start = 0;
    private long position = 0;
    private int documentsRead = 0;
    private int documentsNumber = 0;
    private FSDataInputStream inputStream;
    private final int MAX_SIZE = 2048;

    @Override
    public void initialize(InputSplit is, TaskAttemptContext tac) throws IOException, InterruptedException {
        CompressedFileSplit split = (CompressedFileSplit) is;
        final Path path = split.getPath();
        Configuration conf = tac.getConfiguration();
        FileSystem fs = path.getFileSystem(conf);

        inputStream = fs.open(path);
        start = split.getStart();
        position = start;
        inputStream.seek(position);

        documentSizes = split.getDocumentSizes();
        documentsNumber = documentSizes.size();



    }
    @Override
    public boolean nextKeyValue() throws IOException, InterruptedException {
        if (documentsRead >= documentsNumber) {
            valueDocument = new Text();
            keyOffset = new LongWritable();
            return false;
        }
        valueDocument.clear();

        int newSize = documentSizes.get(documentsRead);
        byte[] bytesDocument = new byte[newSize];
        inputStream.readFully(bytesDocument, 0, newSize);


        Inflater decompressor = new Inflater();
        decompressor.setInput(bytesDocument);

        byte[] buffer = new byte[MAX_SIZE];
        while (true) {
            try {
                int bytesDecompressed = decompressor.inflate(buffer);
                if (bytesDecompressed > 0) {
                    valueDocument.append(buffer, 0, bytesDecompressed);
                } else {
                    break;
                }
            } catch (DataFormatException exception) {
                break;
            }
        }
        decompressor.end();

        documentsRead++;
        position += newSize;
        return true;

    }
    @Override
    public LongWritable getCurrentKey() throws IOException, InterruptedException {
        return keyOffset;
    }
    @Override
    public Text getCurrentValue() throws IOException, InterruptedException {
        return valueDocument;
    }
    @Override
    public float getProgress() throws IOException, InterruptedException {
        return (float)documentsRead/documentsNumber;

    }
    @Override
    public void close() throws IOException {
        inputStream.close();

    }
}




