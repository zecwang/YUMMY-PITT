import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;

public class IdSet {
    public static void main(String[] args) {
        HashSet<String> ids = getIdSet();
        System.out.println(ids);
        System.out.println(ids.size());
    }

    public static HashSet<String> getIdSet() {
        File file = new File("src/data/" + Config.DIR + "/ids.txt");
        BufferedReader reader;
        HashSet<String> ids = new HashSet<>();
        try {
            reader = new BufferedReader(new FileReader(file));
            String line;
            while ((line = reader.readLine()) != null) {
                ids.add(line);
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return ids;
    }
}
