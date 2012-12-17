package GM.music;
import java.util.*;

public class SongPhraseIterator {

    Iterator<Part> partIter=null;
    Iterator<Phrase> phraseIter=null;
    public SongPhraseIterator(Song song) {
        partIter = song.parts.iterator();
        if (partIter.hasNext()) phraseIter = partIter.next().phrases.iterator();
    }

    public boolean hasNext() {
        if (phraseIter == null) return false;
        if (phraseIter.hasNext()) return true;
        while (partIter.hasNext()) {
            phraseIter = partIter.next().phrases.iterator();
            if (phraseIter.hasNext()) return true;
        }
        return false;
    }

    public Phrase next() {
        if (phraseIter.hasNext()) return phraseIter.next();
        else phraseIter = partIter.next().phrases.iterator();
        return phraseIter.next();
    }
}
