import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;

import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.Job;

import org.apache.hadoop.util.GenericOptionsParser;

import java.io.IOException;

import java.util.HashSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class DocumentFrequencyCounter {


    public static class CountingMapper extends Mapper<Object, Text, Text, IntWritable> {
        private Text term = new Text();
        private IntWritable one = new IntWritable();
        private Pattern pattern = Pattern.compile("\\p{L}+");


        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            String valString = value.toString().toLowerCase();
            Matcher matcher = pattern.matcher(valString);

            HashSet<String> terms = new HashSet<>();
            while (matcher.find()) {
                terms.add(matcher.group());

            }
            for (String s: terms) {
                term.set(s);
                context.write(term, one);
            }

        }
    }

    public static class CountingReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {

            int count = 0;
            for (IntWritable val : values) {
                count += 1;
            }
            IntWritable df = new IntWritable(count);
            context.write(key, df);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: DocumentFrequencyCounter <in> <out>");
            System.exit(2);
        }
        Job job = new Job(conf, "Document Frequency Counter");

        job.setJarByClass(DocumentFrequencyCounter.class);

        job.setInputFormatClass(CompressedFileInputFormat.class);

        job.setMapperClass(CountingMapper.class);
        job.setReducerClass(CountingReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
