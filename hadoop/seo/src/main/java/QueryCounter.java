import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;
import java.net.URI;

public class QueryCounter extends Configured implements Tool {
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

    public static class CountingMapper extends Mapper<Object, Text, HostQueryKey, IntWritable> {
        private HostQueryKey hostQuery = new HostQueryKey();
        private IntWritable one = new IntWritable(1);

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            String[] tokens = value.toString().split("\t");
            String query = tokens[0];
            String url = tokens[1];
            String host = getDomainName(url);

            hostQuery.set(host, query);
            context.write(hostQuery, one);



        }
    }
    public static class CountingReducer extends Reducer<HostQueryKey, IntWritable, Text, Text> {
        private Text queryFrequency = new Text();

        public void reduce(HostQueryKey key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {

            Configuration conf = context.getConfiguration();
            String minclicksString = conf.get("seo.minclicks");
            boolean minclicksIsSet = (minclicksString != null);
            int minclicks = 0;
            if (minclicksIsSet) {
                minclicks = Integer.parseInt(minclicksString);
            }



            //OH MY GOD KEY CHANGES WHILE WE ITERATE THROUGH VALUES IT'S FANTASTIC
            String currentQuery = "";
            String newQuery = "";
            int currentQueryFrequency = 0;
            int newQueryFrequency = 0;
            String maxQuery = "";
            int maxQueryFrequency = 0;



            for (IntWritable value: values){
                newQuery = key.getQuery().toString();
                newQueryFrequency = value.get();
                if (!newQuery.equals(currentQuery)) {
                    if (!currentQuery.equals("")) {
                        /*queryFrequency.set(currentQuery + "\t" + Integer.toString(currentQueryFrequency));
                        context.write(key.getHost(), queryFrequency);*/
                        if (currentQueryFrequency  > maxQueryFrequency) {
                            maxQuery = currentQuery;
                            maxQueryFrequency = currentQueryFrequency;
                            // the queries are sorted lexicographically so we'll automatically choose the first query among queries with the sam frequency
                        }
                    }
                    currentQuery = newQuery;
                    currentQueryFrequency = 0;
                }
                currentQueryFrequency += newQueryFrequency;

            }

            /*queryFrequency.set(currentQuery + "\t" + Integer.toString(currentQueryFrequency));
            context.write(key.getHost(), queryFrequency);*/
            if (currentQueryFrequency  > maxQueryFrequency) {
                maxQuery = currentQuery;
                maxQueryFrequency = currentQueryFrequency;
            }
            queryFrequency.set(maxQuery + "\t" + Integer.toString(maxQueryFrequency));
            if (!minclicksIsSet || maxQueryFrequency >= minclicks) {
                context.write(key.getHost(), queryFrequency);
            }

        }
    }

    @Override
    public int run(String[] args) throws Exception {
        Configuration conf = this.getConf();

        Job job = new Job(conf, "QueryCounter");
        job.setJarByClass(QueryCounter.class);
        job.setMapperClass(CountingMapper.class);
        job.setReducerClass(CountingReducer.class);

        job.setMapOutputKeyClass(HostQueryKey.class);
        job.setMapOutputValueClass(IntWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        job.setPartitionerClass(HostHashPartitioner.class);
        job.setGroupingComparatorClass(HostQueryGroupingComparator.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception {
        // Let ToolRunner handle generic command-line options
        int res = ToolRunner.run(new Configuration(), new QueryCounter(), args);

        System.exit(res);
    }

}