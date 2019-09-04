
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;

public class HostQueryKey implements WritableComparable<HostQueryKey> {

    private Text host;
    private Text query;


    public HostQueryKey() {
        this.host = new Text();
        this.query = new Text();
    }

    public void set(String h, String q) {
        this.host.set(h);
        this.query.set(q);
    }

    @Override
    public void readFields(DataInput dataInput) throws IOException {
        host.readFields(dataInput);
        query.readFields(dataInput);
    }

    @Override
    public void write(DataOutput dataOutput) throws IOException {
        host.write(dataOutput);
        query.write(dataOutput);
    }

    @Override
    public String toString() {
        return host.toString() + "\t" + query.toString();
    }

    @Override
    public int compareTo (HostQueryKey other) {
        int result;
        result = host.compareTo(other.getHost());
        if (result == 0) {
            result = query.compareTo(other.getQuery());
        }
        return result;
    }

    public Text getHost() {
        return host;
    }

    public Text getQuery() {
        return query;
    }



}