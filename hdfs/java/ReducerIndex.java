package org.example;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ReducerIndex extends Reducer<Text, Text, Text, Text> {
    private final Text allFilesConcatValue = new Text();
    private final StringBuilder fileList = new StringBuilder();
    private static final int BATCH_SIZE = 1000;

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws java.io.IOException, InterruptedException {
        fileList.setLength(0); // Clear StringBuilder for the entire reduce task
        int count = 0;

        // Since values are not reusable, create a local copy to iterate multiple times if needed
        List<String> valueList = new ArrayList<>();
        for (Text value : values) {
            valueList.add(value.toString());
        }

        // Build the continuous string without newlines
        for (String value : valueList) {
            // value is in format "filename:count"
            String[] parts = value.split(":");
            if (parts.length != 2) continue; // Skip malformed entries
            String filename = parts[0];
            String countStr = parts[1];

            // Format: Word;Url;Count| (no newline)
            fileList.append(key.toString()).append(";")
                    .append(filename).append(";")
                    .append(countStr).append("|");

            count++;
            if (count >= BATCH_SIZE) {
                // Write the batch without forcing a newline
                allFilesConcatValue.set(fileList.toString());
                context.write(new Text(""), allFilesConcatValue);
                fileList.setLength(0); // Clear for the next batch
                count = 0;
            }
        }

        // Write any remaining records in a single call
        if (fileList.length() > 0) {
            allFilesConcatValue.set(fileList.toString());
            context.write(new Text(""), allFilesConcatValue);
        }

        // Clear StringBuilder at the end
        fileList.setLength(0);
    }
}