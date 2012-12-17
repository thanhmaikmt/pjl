package GM.jdbc;

import java.io.InputStream;
import java.io.StringBufferInputStream;

public class BinaryData {
    InputStream in;
    int n;
    public BinaryData(String str) {
        in=new StringBufferInputStream(str);
        n=str.length();
    }
}
