
package GM;

/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */
import javax.swing.*;
import com.softsynth.jsyn.*;

import java.awt.event.*;

public class UsageDisp  implements ActionListener {


    /**
     * run
     */
    public void actionPerformed(ActionEvent event) {
        System.out.println(Synth.getSharedContext().getUsage());
    }

}
