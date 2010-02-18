/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package redcode;

import javax.swing.table.AbstractTableModel;

/**
 *
 * @author pjl
 */
class CodeTableModel  extends AbstractTableModel {
    private final Machine mach;

    CodeTableModel(Machine mach){
        this.mach=mach;
    }

    public String getColumnName(int columnIndex) {
        switch (columnIndex) {

            case 0: return "addr";
            case 1: return "machine code";
            case 2: return "opcode";
            case 3: return "A";
            case 4: return "B";

        }
        return "";
    }

    public int getRowCount() {
        return mach.getSize();
    }

    public int getColumnCount() {
        return 5;
    }

    public Object getValueAt(int rowIndex, int columnIndex) {
        switch (columnIndex) {
            case 0: return ""+rowIndex;
            case 1: return mach.mem[rowIndex].word.binaryString() ;// + " #"+ mach.mem[rowIndex].word.x;
            case 2: return mach.opCodeAt(rowIndex);
            case 3: return mach.operandAAt(rowIndex);
            case 4: return mach.operandBAt(rowIndex);

        }
        assert(false);
        return null;
    }

}
