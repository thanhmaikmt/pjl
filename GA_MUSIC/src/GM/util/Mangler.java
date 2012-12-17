package GM.util;

public class Mangler {

    private static String key="1%.\"add@(term";

    public static char [] spin(char [] str)
    {
        char [] sb = new char[str.length];

        int lenStr = str.length;
        int lenKey = key.length();
        for ( int i = 0, j = 0; i < lenStr; i++, j++ )  {
            if ( j >= lenKey ) j = 0;
            sb[i] = (char)(str[i] ^ key.charAt(j));
        }
        return sb;
    }


}

