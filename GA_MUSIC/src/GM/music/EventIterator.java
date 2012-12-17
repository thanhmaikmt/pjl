package GM.music;


import java.util.*;

public class EventIterator {


    public EventIterator(EventList list) {
	this(list, Time.ZERO, Time.INF);
    }

    public EventIterator(EventList list,Time fromA,Time tillA) {
	from = fromA;
	till = tillA;
	iter = list.iterator();

	while(iter.hasNext()) {
	    next = (Event)iter.next();
 	    if ( next.getTime().compareTo(from) >= 0.0) {
 		if (  next.getTime().compareTo(till) > 0.0) next = null;
 		return;
 	    }
	}
	next = null;
    }
	
	
	
    public Event next() {
	if (next == null) return null;

	Event tmp=next;
	
	if (iter.hasNext() ) {
	    next = (Event)iter.next();
	    if ( next.getTime().compareTo(till) >= 0 ) next = null;
	} else {
	    next = null;
	}
	return tmp;
    }    

    public Event peek() {
	return next;
    }

    public boolean hasNext() {
	return next != null;
    }



    private Event   next;
    private Iterator iter;
    private Time    from;
    private Time    till;
}
