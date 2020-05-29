import java.io.*;
import java.util.HashSet;

public class UsersExt {
    public static void main(String[] args) {
        File file = new File("src/data/yelp_academic_dataset_user.json");
        BufferedReader reader;
        String outputName = "src/data/" + Config.DIR + "/user.json";
        BufferedWriter writer;
        HashSet<String> users = UsersIdSet.getUsersIdSet();
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
                String[] strings = line.split("\",");
                if (users.contains(strings[0].split(":")[1].replaceAll("\"", ""))) {
                    for (String str : strings) {
                        if (str.contains("friends")) {
                            String idGroup = str.split(":\"")[1];
                            String[] ids = idGroup.split(", ");
                            for (String id : ids) {
                                if (!users.contains(id)) {
                                    line = line.replaceAll(id + ", ", "");
                                    line = line.replaceAll(id, "");
                                }
                            }
                        }
                    }
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
