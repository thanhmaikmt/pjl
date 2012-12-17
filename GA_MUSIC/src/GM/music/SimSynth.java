package GM.music;

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
public interface SimSynth {
  //  public IdString[] getBankNames();
    public Voice createVoice(GMPatch pat) throws Exception;
    public Conductor getConductor() throws Exception;
   //  public Bank[] getBanks();
    public String getName();
}
