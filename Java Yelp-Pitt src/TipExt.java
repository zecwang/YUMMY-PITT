import java.io.*;
import java.util.HashSet;

public class TipExt {
    public static void main(String[] args) {
        File file = new File("src/data/yelp_academic_dataset_tip.json");
        BufferedReader reader;
        String outputName = "src/data/" + Config.DIR + "/tip.json";
        BufferedWriter writer;
        HashSet<String> ids = IdSet.getIdSet();
        try {
            File output = new File(outputName);
            if (!output.exists()) {
                File dir = new File(output.getParent());
                dir.mkdirs();
                output.createNewFile();
            }
            reader = new BufferedReader(new FileReader(file));
            writer = new BufferedWriter(new FileWriter(outputName));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] strings = line.split(",");
                if (ids.contains(strings[1].split(":")[1])) {
                    writer.write(line);
                    writer.newLine();
                }
            }
            writer.close();
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
