import org.apache.hadoop.fs.Path;

import org.apache.hadoop.mapred.FileSplit;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import java.util.ArrayList;



public class CompressedFileSplit extends FileSplit {
    ArrayList<Integer> documentSizes;
    public CompressedFileSplit() {
        super();
        //oh my gosh java why don't you just add default constructor by yourself
    }

    public CompressedFileSplit(Path file, long start, long length, String[] hosts, ArrayList<Integer> documentSizes) {
        super(file, start, length, hosts);
        setDocumentSizes(new ArrayList<>(documentSizes));
    }


    public ArrayList<Integer> getDocumentSizes() {
        return documentSizes;
    }

    public void setDocumentSizes(ArrayList<Integer> documentSizes) {
        this.documentSizes = documentSizes;
    }

    protected void readDocumentsSizes(DataInput in) throws IOException {
        ArrayList<Integer> read = new ArrayList<>();
        int size = in.readInt();
        for (int i = 0; i < size ; i++) {
            read.add(in.readInt());
        }
        setDocumentSizes(read);

    }

    protected void writeDocumentSizes(DataOutput out) throws IOException {
        out.writeInt(documentSizes.size());
        for (Integer size : documentSizes) {
            out.writeInt(size);
        }
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        super.readFields(in);
        readDocumentsSizes(in);
    }

    @Override
    public void write(DataOutput out) throws IOException {
        super.write(out);
        writeDocumentSizes(out);

    }


}
