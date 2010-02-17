/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redcode;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.Observable;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author pjl
 */
public class Machine extends Observable {

    static private final int nBitOperand = 6;
    Instruction mem[];
    int PC;
    int size;
    private int parseLine = 0;
    String status="";
    private boolean running=false;
    private boolean inputWait=false;

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
        Thread t=new Thread(new Runnable(){

            public void run() {
                while(running) {
                    try {
                        step();
                    } catch (RedCodeParseException ex) {
                        Logger.getLogger(Machine.class.getName()).log(Level.SEVERE, null, ex);
                    }
                }
            }
            
        });
        running=true;
        t.start();
    }

    void stop() {
        running=false;
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

    enum Mode {

        IMEDIATE("#"), DIRECT(""), INDIRECT("@");
        String s;

        Mode(String s) {
            this.s = s;
        }

        @Override
        public String toString() {
            return s;
        }
    };

    enum Opcode {

        HLT("HLT"), ADD("ADD"), MOV("MOV"), SUB("SUB"), DAT("DAT"), JMP("JMP"), JMZ("JMZ"), DJZ("DJZ"), CMP("CMP"), IN("IN"), OUT("OUT");
        String name;

        Opcode(String name) {
            this.name = name;
        }

        @Override
        public String toString() {
            return name;
        }
    };

    String getStatus() {
        if (inputWait) return "Waiting for input";
        if (running) return "Running";
        if (mem[PC].code == Opcode.HLT) return "Halted";
        if (mem[PC].code == Opcode.DAT) return "Halted (invalid instruction)";
        assert(false);
        return "";
    }

    Machine(int size) throws RedCodeParseException {
        this.size = size;
        mem = new Instruction[size];
        for (int i = 0; i < size; i++) {
            mem[i] = new Instruction("DAT 0");
        }
    }

    void load(BufferedReader reader) throws RedCodeParseException {
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

    public class Instruction {

        Value word;
        Opcode code;
        Operand opA;
        Operand opB;

        Instruction(String line1) throws RedCodeParseException {
            String line = line1.trim();

            word = new Value();
            String toks[] = line.split("[ \t]+");

            for (Opcode op : Opcode.values()) {
                if (toks[0].equals(op.name)) {
                    code = op;
                }
            }

            switch (code) {
                case DAT:
                    if (toks.length < 2) {
                        throw new RedCodeParseException(" Expected an operand!", "");
                    }
                    opB = new OperandB(toks[1]);
                    return;
                case JMP:
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
                case HLT:
                    running=false;
                    break;

                case DAT:
                    running=false;
                   break;

                case CMP:
                    if (opA.getOpValue() == opB.getOpValue()) {
                        PC = (PC + 1) % size;
                    } else {
                        PC = (PC + 2) % size;
                    }
                    break;

                case DJZ:
                    opB.putOpValue(opB.getOpValue() - 1);
                case JMZ:
                    if (opB.getOpValue() != 0) {
                        PC = (PC + 1) % size;
                        break;
                    }
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
                        int val = opA.getOpValue();
                        opB.putOpValue(val);
                        assert (opB.getOpValue() == val);
                    } else if (opA.mode == Mode.DIRECT) {

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
            if (opA != null) {
                return code.name + " " + opA.toString() + " " + opB.toString();
            }
            return code.name + "     " + opB.toString();
        }

        abstract class Operand {

            BitSection bits;
            Mode mode;

            Operand(String str1, BitSection bits) throws RedCodeParseException {

                String str = str1.trim();
                this.bits = bits;
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
            }

            private void putOpValue(int val) {
                int adr = resolveAddress();
                mem[adr].opB.bits.put(val);
            }

            private int resolveAddress() {

                int vv = bits.get();

                switch (mode) {
                    case DIRECT:
                        return (size + PC + vv) % size;

                    case INDIRECT:
                        int ad1 = (size + PC + vv) % size;
                        return (size + ad1 + mem[ad1 % size].opB.getValue()) % size;
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
                        return (size + PC + bits.get()) % size;
                    case INDIRECT:
                        int ad1 = PC + bits.get();
                        return (size + ad1 + mem[ad1 % size].opB.getValue()) % size;

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
                super(str, new BitSection(word, 0, nBitOperand));
            }
        }

        class OperandB extends Operand {

            OperandB(String str) throws RedCodeParseException {
                super(str, new BitSection(word, nBitOperand, nBitOperand));
            }
        }
    }

    void step() throws RedCodeParseException {
        mem[PC].execute();
    }

    @Override
    public String toString() {
        String str = "";
        for (Instruction inst : mem) {
            str = str + inst.toString() + "\n";
        }
        return str;
    }
}
