import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;

import java.io.EOFException;
import java.io.IOException;

import java.util.ArrayList;
import java.util.List;


public class CompressedFileInputFormat extends FileInputFormat<LongWritable, Text> {
    @Override
    public RecordReader<LongWritable, Text> createRecordReader (InputSplit split, TaskAttemptContext context) {
        return new CompressedRecordReader();
        // initialize seems to be called by the framework
    }


    @Override
    public List<InputSplit> getSplits(JobContext job) throws IOException {
        Configuration conf = job.getConfiguration();
        long bytesPerSplit = conf.getLong("mapreduce.input.indexedgz.bytespermap", 32L * 1024L * 1024L);
        List<InputSplit> splits = new ArrayList<>();

        for (FileStatus status: listStatus(job)) {
            Path documentsPath = status.getPath();
            Path documentSizesPath = documentsPath.suffix(".idx");
            FileSystem fs = documentsPath.getFileSystem(conf);
            FSDataInputStream documentSizesInputStream = fs.open(documentSizesPath);

            long position = 0;
            long splitSize = 0;
            ArrayList<Integer> documentSizes = new ArrayList<>();
            while (true) {
                int documentSize = 0;
                try {
                    documentSize = Integer.reverseBytes(documentSizesInputStream.readInt());
                } catch (EOFException exception) {
                    break;
                }

                splitSize += (long) documentSize;
                documentSizes.add(documentSize);
                if (splitSize >= bytesPerSplit) {
                    splits.add(new CompressedFileSplit(documentsPath, position, splitSize, new String[]{}, documentSizes));
                    position += splitSize;
                    splitSize = 0;
                    documentSizes.clear();
                }
            }
            if (!documentSizes.isEmpty()) {
                splits.add(new CompressedFileSplit(documentsPath, position, splitSize, new String[]{}, documentSizes));
            }

            documentSizesInputStream.close();
        }

        return splits;
    }
}
