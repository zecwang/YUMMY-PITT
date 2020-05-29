import java.io.*;

public class BusinessExt {
    public static void main(String[] args) {
        File file = new File("src/data/yelp_academic_dataset_business.json");
        BufferedReader reader;
        String outputName = "src/data/" + Config.DIR + "/business.json";
        BufferedWriter writer;
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
                if (line.contains(Config.CITY)) {
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
