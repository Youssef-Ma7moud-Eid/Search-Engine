package org.example;
import java.io.IOException;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.util.StringUtils;

public class MapperIndex extends Mapper<LongWritable, Text, Text, Text> {
    private Text keyInfo = new Text();
    private Text valueInfo = new Text();
    private FileSplit split;

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        this.split = (FileSplit) context.getInputSplit();
        String fullPath = split.getPath().getName(); // Get the full filename (e.g., URL-encoded with extension)

        // Extract filename without extension
        String filename;
        int lastDotIndex = fullPath.lastIndexOf(".");
        if (lastDotIndex != -1 && lastDotIndex > 0) {
            // Extension found, extract up to the last dot
            filename = fullPath.substring(0, lastDotIndex);
        } else {
            // No extension, use the entire filename
            filename = fullPath;
            context.getCounter("Mapper", "NoExtensionFiles").increment(1); // Track files with no extension
        }

        // Skip hidden files (e.g., .gitignore) or empty filenames
        if (filename.startsWith(".") || filename.isEmpty()) {
            context.getCounter("Mapper", "SkippedInvalidFilename").increment(1); // Track skipped files
            return;
        }

        // Hash the filename if it's too long (e.g., > 200 characters to stay safe)
        if (filename.length() > 200) {
            filename = hashFilename(filename); // Convert to a fixed-length hash
            context.getCounter("Mapper", "LongFilenamesHashed").increment(1); // Track hashed filenames
        }

        StringTokenizer tokenizer = new StringTokenizer(value.toString());

        while (tokenizer.hasMoreTokens()) {
            String word = tokenizer.nextToken();
            // Combine word and filename, truncate if too long
            String combinedKey = word + "@" + filename;
            if (combinedKey.length() > 200) { // Arbitrary limit to avoid key overflow
                combinedKey = combinedKey.substring(0, 200);
                context.getCounter("Mapper", "TruncatedKeys").increment(1); // Track truncated keys
            }
            this.keyInfo.set(combinedKey);
            this.valueInfo.set("1");
            context.write(this.keyInfo, this.valueInfo);
        }
    }

    // Helper method to hash filename
    private String hashFilename(String filename) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] messageDigest = md.digest(filename.getBytes());
            BigInteger no = new BigInteger(1, messageDigest);
            String hash = no.toString(16);
            while (hash.length() < 32) {
                hash = "0" + hash; // Pad to 32 characters
            }
            return hash;
        } catch (NoSuchAlgorithmException e) {
            // Fallback to truncated filename if hashing fails
            return filename.substring(0, 200);
        }
    }
}