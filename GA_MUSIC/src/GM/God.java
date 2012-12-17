package GM;


import java.io.File;
import java.net.URL;
import java.net.MalformedURLException;

/**
 * Write a description of class God here.
 *
 * @author DR pJ
 * @version 1
 */
public class God {
    /**
     * God is static (just one tee hee)
     */

    static public String sampleURL
            = new File(System.getProperty("user.dir"), "samples").toURI().toString();


    public static URL resolveSampleURL(String sampName) throws MalformedURLException {
        return new URL(sampleURL+"/"+sampName.trim());
    }

}
