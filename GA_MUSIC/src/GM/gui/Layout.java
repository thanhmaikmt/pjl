package GM.gui;

import GM.music.Time;

public class Layout {
    static int width=800;
    static int height=600;

    static int partCntrlHeight=100;
    static int partViewHeight=60;
    static int timeLineHeight=15;

    static int phraseCntrlHeight = partCntrlHeight;
    static int playerViewWidth = 250;

    static int headerHeight = partViewHeight+timeLineHeight;
    static int dragPanelWidth = 20;
    static int dragPanelHeight = 20;

    static int tabHeight() {
        return partCntrlHeight +
                partViewHeight +
                timeLineHeight;
    }

    static int tabWidth=200;
    static int trackHeight=40;
    static int rightWidth=width-tabWidth;

    static double pianoRollScale = 16.0/Time.bitsPerBeat;
}
