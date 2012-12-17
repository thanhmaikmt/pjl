package GM.music;
// import gm.*;

import java.util.*;

public class EventList extends TreeSet<Event>
{

    public EventList() {

    }

    public EventList(EventList e) {
        Iterator<Event> iter=e.iterator();
        while(iter.hasNext()) add(iter.next());
    }

}
