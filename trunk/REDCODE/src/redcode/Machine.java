/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redcode;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.util.Observable;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.Timer;

/**
 *
 * @author pjl
 */
public class Machine extends Observable {

    enum Mode {

        IMEDIATE("#", 1), DIRECT("", 0), INDIRECT("@", 2);
        String s;
        int val;

        Mode(String s, int val) {
            this.s = s;
            this.val = val;
        }

        @Override
        public String toString() {
            return s;
        }
    };

    enum Opcode {

        HLT("HLT", 1), ADD("ADD", 2), MOV("MOV", 3), SUB("SUB", 4),
        DAT("DAT", 0), JMP("JMP", 5), JMG("JMG", 6), JMZ("JMZ", 7),
        DJZ("DJZ", 8), CMP("CMP", 9), IN("IN", 10), OUT("OUT", 11);
        String name;
        int val;

        Opcode(String name, int val) {
            this.name = name;
            this.val = val;
        }

        @Override
        public String toString() {
            return name;
        }
    };
    static private final int nBitOperand = 8;
    static private final int nBitOpcode = 4;
    static private final int nBitMode = 2;
    Instruction mem[];
    int PC;
    int size;
    private int parseLine = 0;
    String status = "";
    private boolean running = false;
    private boolean inputWait = false;
    private Timer timer;
    private IO io;

    Machine(int size) throws RedCodeParseException {
        this.size = size;
        init();
    }

    void setIO(IO io) {
        this.io = io;
    }

    int getSize() {
        return size;
    }

    Object opCodeAt(int rowIndex) {
        return mem[rowIndex].code.toString();
    }

    Object operandAAt(int rowIndex) {
        if (mem[rowIndex].opA == null) {
            return "";
        }
        return mem[rowIndex].opA.toString();
    }

    Object operandBAt(int rowIndex) {
        if (mem[rowIndex].opB == null) {
            return "";
        }

        return mem[rowIndex].opB.toString();
    }

    int getPC() {
        return PC;
    }

    int getParseLine() {
        return parseLine;
    }

    void run() {

        timer = new Timer(500, new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                try {
                    step();
                } catch (RedCodeParseException ex) {
                    Logger.getLogger(Machine.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        });

        timer.start();
    }

    void stop() {
        running = false;
        if (timer == null) {
            return;
        }
        timer.stop();
        timer = null;
    }

    void setSize(int sizeNew) {
        Instruction memNew[] = new Instruction[sizeNew];

        for (int i = 0; i < sizeNew; i++) {

            if (i < size) {
                memNew[i] = mem[i];
            } else {
                try {
                    memNew[i] = new Instruction("DAT 0");
                } catch (RedCodeParseException ex) {
                    Logger.getLogger(Machine.class.getName()).log(Level.SEVERE, null, ex);
                }
            }


        }
        size = sizeNew;
        mem = memNew;
        setChanged();
        notifyObservers();

    }

    String getStatus() {
        if (inputWait) {
            return "Waiting for input";
        }
        if (running) {
            return "Running";
        }
        if (mem[PC].code == Opcode.HLT) {
            return "Halted";
        }
        if (mem[PC].code == Opcode.DAT) {
            return "Halted (invalid instruction)";
        }
        assert (false);
        return "";
    }

    void init() throws RedCodeParseException {
        mem = new Instruction[size];
        for (int i = 0; i < size; i++) {
            mem[i] = new Instruction("DAT 0");
        }
    }

    void load(BufferedReader reader) throws RedCodeParseException {
        init();
        parseLine = 0;
        boolean pcSet = false;
        setChanged();
        String str1 = null;
        int loc = 0;
        while (true) {
            try {
                str1 = reader.readLine();

                if (str1 == null) {
                    break;
                }
                String str = str1.trim();
                if (str.isEmpty()) {
                    break;
                }
                mem[loc] = new Instruction(str);
                if ((!pcSet) && mem[loc].code != Opcode.DAT) {
                    PC = loc;
                    pcSet = true;
                }

                loc++;
                parseLine++;
            } catch (IOException ex) {

                Logger.getLogger(Machine.class.getName()).log(Level.SEVERE, null, ex);
                throw new RedCodeParseException(str1, ex.getMessage());
            }
        }
        notifyObservers();
        return;
    }

    void step() throws RedCodeParseException {
        
//        // Do this on another thread to avoid deadlock
//        new Thread(new Runnable() {
//
//            public void run() {
                mem[PC].execute();
//            }
//        }).run();

    }

    @Override
    public String toString() {
        String str = "";
        for (Instruction inst : mem) {
            str = str + inst.toString() + "\n";
        }
        return str;
    }

    int fixAddress(int addr) {
        while (addr < 0) {
            addr += size;
        }
        return addr % size;
    }

    class Value {

        int x;
        private final int nBit;

        Value(int nBit) {
            this.nBit = nBit;
        }

        public String binaryString() {
            String str = "";

            int mask = 1;
            for (int i = 0; i < nBit; i++) {
                if (i == nBitOperand ||
                        i == 2 * nBitOperand ||
                        i == 2 * nBitOperand + nBitMode ||
                        i == 2 * nBitOperand + 2 * nBitMode) {
                    str = "|" + str;
                }

                if ((x & mask) != 0) {
                    str = "1" + str;
                } else {
                    str = "0" + str;
                }
                mask = mask * 2;

            }
            return str;

        }
    }

    public class Instruction {

        Value word = new Value(nBitOperand * 2 + 2 * nBitMode + nBitOpcode);
        Opcode code;
        Operand opA;
        Operand opB;
        UBitSection bitOpcode = new UBitSection(word, (nBitOperand + nBitMode) * 2, nBitOpcode);
        UBitSection bitOpAmode = new UBitSection(word, nBitOperand * 2 + nBitMode, nBitMode);
        UBitSection bitOpBmode = new UBitSection(word, nBitOperand * 2, nBitMode);
        BitSection bitOpB = new BitSection(word, 0, nBitOperand);
        BitSection bitOpA = new BitSection(word, nBitOperand, nBitOperand);

        Instruction(String line1) throws RedCodeParseException {
            String line = line1.trim();

            String toks[] = line.split("[ \t]+");

            for (Opcode op : Opcode.values()) {
                if (toks[0].equals(op.name)) {
                    code = op;
                    bitOpcode.put(code.val);
                }
            }

            if (code == null) {
                throw new RedCodeParseException("Invalid line " + line1, "");
            }

            switch (code) {
                case DAT:
                    if (toks.length < 2) {
                        throw new RedCodeParseException(" Expected an operand!", "");
                    }
                    opB = new OperandB(toks[1]);
                    return;
                case JMP:
                case OUT:
                case IN:
                    if (toks.length < 2) {
                        throw new RedCodeParseException(" Expected an operand!", "");
                    }
                    opA = new OperandB(toks[1]);
                    return;
                case HLT:
                    return;
                default:
                    if (toks.length < 3) {
                        throw new RedCodeParseException(" Expected 2 operands !", "");
                    }
                    opA = new OperandA(toks[1]);
                    opB = new OperandB(toks[2]);
            }
        }

        void execute() {

            switch (code) {
                case OUT:
                    io.put(opA.getOpValue());
                    PC = (PC + 1) % size;
                    break;

                case IN:
                    Integer val = io.get();
                    if (val == null) return;
                    
                    opA.putOpValue(val);
                    PC = (PC + 1) % size;
                    break;


                case HLT:
                    running = false;
                    break;

                case DAT:
                    running = false;
                    break;

                case CMP:
                    if (opA.getOpValue() == opB.getOpValue()) {
                        PC = (PC + 1) % size;
                    } else {
                        PC = (PC + 2) % size;
                    }
                    break;
                case JMG:
                    if (opB.getOpValue() <= 0) {
                        PC = (PC + 1) % size;
                        break;
                    }
                    PC = opA.getAddress();
                    break;


                case DJZ:
                    opB.putOpValue(opB.getOpValue() - 1);
                case JMZ:
                    if (opB.getOpValue() != 0) {
                        PC = (PC + 1) % size;
                        break;
                    }
                    PC = opA.getAddress();
                    break;

                // fall thru
                case JMP:
                    PC = opA.getAddress();
                    break;

                case ADD:
                    opB.putOpValue(opA.getOpValue() + opB.getOpValue());
                    PC = (PC + 1) % size;
                    break;

                case SUB:
                    opB.putOpValue(opB.getOpValue() - opA.getOpValue());
                    PC = (PC + 1) % size;
                    break;

                case MOV:
                    if (opA.mode == Mode.IMEDIATE) {
                        val = opA.getOpValue();
                        opB.putOpValue(val);
                        if (opB.getOpValue() != val) {
                            System.out.println(opB.getOpValue() + "   " + val);
                            //                    assert(false);

                        }
                    } else {  // if (opA.mode == Mode.DIRECT) {

                        int addrA = opA.getAddress();
                        int addrB = opB.getAddress();

                        Instruction cpy = null;
                        try {
                            cpy = (Instruction) mem[addrA].copy();
                        } catch (RedCodeParseException ex) {
                            Logger.getLogger(Machine.class.getName()).log(Level.SEVERE, null, ex);
                            assert (false);
                        }
                        mem[addrB] = cpy;


                    }
                    PC = (PC + 1) % size;
            }
            setChanged();
            notifyObservers();
        }

        public Object copy() throws RedCodeParseException {
            return new Instruction(toString());
        }

        @Override
        public String toString() {
            String ret = code.name;
            if (opA != null) {
                ret = ret + " " + opA.toString();
            }
            if (opB != null) {
                ret = ret + " " + opB.toString();
            }
            return ret;
        }

        abstract class Operand {

            BitSection bits;
            UBitSection bitsMode;
            Mode mode;

            Operand(String str1, BitSection bits, UBitSection modeBit) throws RedCodeParseException {

                String str = str1.trim();
                this.bits = bits;
                this.bitsMode = modeBit;

                if (str.startsWith("@")) {
                    mode = Mode.INDIRECT;
                    str = str.substring(1);
                } else if (str.startsWith("#")) {
                    mode = Mode.IMEDIATE;
                    str = str.substring(1);
                } else {
                    mode = Mode.DIRECT;
                }
                try {
                    int val = Integer.parseInt(str);
                    bits.put(val);
                } catch (Exception ex) {
                    throw new RedCodeParseException(str, ex.getMessage());
                }
                modeBit.put(mode.val);
            }

            private void putOpValue(int val) {
                int adr = resolveAddress();
                mem[adr].opB.bits.put(val);
            }

            private int resolveAddress() {

                int vv = bits.get();

                switch (mode) {
                    case DIRECT:
                        return fixAddress(PC + vv);

                    case INDIRECT:
                        int ad1 = fixAddress(PC + vv);
                        return fixAddress(ad1 + mem[ad1].opB.getValue());

                }
                assert (false);
                return -1;
            }

            private int getOpValue() {

                switch (mode) {
                    case IMEDIATE:
                        return bits.get();
                    case DIRECT:
                    case INDIRECT:
                        //int ad1 = (size + PC + vv) % size;
                        return mem[resolveAddress()].opB.getValue();
//                        ad1 = (size + PC + vv) % size;
//                        int ad2 = size + PC + mem[ad1 % size].opB.getValue();
//                        return mem[ad2 % size].opB.getValue();

                }
                assert (false);
                return 0;
            }

            private int getValue() {
                return bits.get();
            }

            private int getAddress() {
                switch (mode) {
                    case DIRECT:
                        return fixAddress(PC + bits.get());
                    case INDIRECT:
                        int ad1 = fixAddress(PC + bits.get());
                        return fixAddress(ad1 + mem[ad1].opB.getValue());

                }
                try {
                    throw new Exception(" getAddress called for imeadiate");
                } catch (Exception ex) {
                    Logger.getLogger(Machine.class.getName()).log(Level.SEVERE, null, ex);
                }
                return 0;
            }

            @Override
            public String toString() {
                return mode.s + getValue();
            }
        }

        class OperandA extends Operand {

            OperandA(String str) throws RedCodeParseException {
                super(str, bitOpA, bitOpAmode);
            }
        }

        class OperandB extends Operand {

            OperandB(String str) throws RedCodeParseException {
                super(str, bitOpB, bitOpBmode);
            }
        }
    }
}
