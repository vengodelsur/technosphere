import java.io.IOException;
import java.net.URISyntaxException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import java.net.URI;


public class HostLister {
    public static String getDomainName(String url) {
        try {
            URI uri = new URI(url);
            String domain = uri.getHost();
            return domain.startsWith("www.") ? domain.substring(4) : domain;
        }
        catch (Exception e) {
            return url;
        }


    }

    public static class ListingMapper extends Mapper<Object, Text, HostQueryKey, IntWritable> {
        private HostQueryKey hostQuery = new HostQueryKey();
        private IntWritable zero = new IntWritable(0);

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            String[] tokens = value.toString().split("\t");
            String query = tokens[0];
            String url = tokens[1];
            String host = getDomainName(url);

            hostQuery.set(host, "");
            context.write(hostQuery, zero);

        }
    }


    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: HostLister <in> <out>");
            System.exit(2);
        }
        Job job = new Job(conf, "HostLister");
        job.setJarByClass(HostLister.class);
        job.setMapperClass(ListingMapper.class);
        //job.setReducerClass(Reducer.class);

        job.setMapOutputKeyClass(HostQueryKey.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setGroupingComparatorClass(HostQueryGroupingComparator.class);

        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}