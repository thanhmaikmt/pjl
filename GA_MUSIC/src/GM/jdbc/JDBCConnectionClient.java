package GM.jdbc;

public interface JDBCConnectionClient {

    public void connectedOK();
    public void statusMessage(String mess);
    public void showProgress(String txt);
}
