import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;

public class UsersIdSet {
    public static void main(String[] args) {
        HashSet<String> users = getUsersIdSet();
        System.out.println(users);
        System.out.println(users.size());
    }

    public static HashSet<String> getUsersIdSet() {
        File file = new File("src/data/" + Config.DIR + "/users_review.txt");
        BufferedReader reader;
        HashSet<String> users = new HashSet<>();
        try {
            reader = new BufferedReader(new FileReader(file));
            String line;
            while ((line = reader.readLine()) != null) {
                users.add(line);
            }
            file = new File("src/data/" + Config.DIR + "/users_tip.txt");
            reader = new BufferedReader(new FileReader(file));
            while ((line = reader.readLine()) != null) {
                users.add(line);
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return users;
    }
}
