import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.io.WritableComparable;

public class HostQueryGroupingComparator extends WritableComparator {
    public HostQueryGroupingComparator() {
        super(HostQueryKey.class, true);
    }
    @Override
    public int compare(WritableComparable wc1, WritableComparable wc2) {
        HostQueryKey key1 = (HostQueryKey) wc1;
        HostQueryKey key2 = (HostQueryKey) wc2;
        return key1.getHost().compareTo(key2.getHost());
    }
}