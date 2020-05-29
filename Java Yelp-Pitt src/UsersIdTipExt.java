import java.io.*;

public class UsersIdTipExt {
    public static void main(String[] args) {
        File file = new File("src/data/" + Config.DIR + "/tip.json");
        BufferedReader reader;
        String outputName = "src/data/" + Config.DIR + "/users_tip.txt";
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
                String[] strings = line.split(",");
                writer.write(strings[0].split(":")[1].replaceAll("\"", ""));
                writer.newLine();
            }
            writer.close();
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
