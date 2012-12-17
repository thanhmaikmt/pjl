package GM.genetic;

import java.util.*;

/**
 * Write a description of class GmRandom here.
 *
 * @author DR pJ
 * @version 1
 */
public class GmRandom extends Random
{
    /**
     * Constructor for objects of class GmRandom
     */
    long seed;
    static Random r= new Random();


    public GmRandom()
    {
        this((new Random()).nextLong());
    }

    public GmRandom(long seed)
    {
        super(seed);
        this.seed=seed;
    }

    static public long  nextSeed() {
        long nseed=r.nextLong();
        nseed = Math.abs(nseed);
        return nseed;
   }

}
