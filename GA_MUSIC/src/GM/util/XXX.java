package GM.util;

public class XXX {


    static int [] toIntArray(char [] c) {
        int x[]= new int[(c.length)];

        for (int i=0;i<c.length;i++) {
            x[i]=c[i];
        }
        return x;
    }


    public static void main(String args[]) {
        String pass="b1valve";
        char [] b= Mangler.spin(pass.toCharArray());
        int x[]=toIntArray(b);

        StringBuffer buff=new StringBuffer("new char[]={");
        for(int i=0;i<x.length;i++) {
            if (i > 0 ) buff.append(","+x[i]);
            else buff.append(x[i]);
        }
        buff.append("}");
        System.out.println(buff);

        char [] z=new char[]{92,21,66,78,20,23,7};

        System.out.println(new String(Mangler.spin(z)));


    }


}
