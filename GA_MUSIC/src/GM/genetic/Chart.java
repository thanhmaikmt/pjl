package GM.genetic;

import GM.jdbc.TableInfoData;

public class Chart {

    static String[] types= {"INT", "INT"};
    static String[] info = {"PerformanceID", "playTime"};
    static public final TableInfoData tableInfo=new TableInfoData(types,info,"ChartTABLE",false);

    long perfId;
    long playTime;

    public String[] getValues() {
        String[] r = {
                     String.valueOf(perfId),
                     String.valueOf(playTime)};
        return r;
    }
    public Chart() {
    }
}
