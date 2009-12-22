/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author pjl
 */
class Boundary {

    Source source;
    Double imp=1.0;

    void setImp(Double imp) {
        this.imp=imp;
    }

    double getValue(double t) {
        if (source == null) return 0.0;
        else return source.getValue(t);
    }

    void setSource(Source src) {
        this.source=src;
    }

}
