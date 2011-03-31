package uk.co.drpj.chimera;

import java.util.Random;

class TargetSpriteMover implements SpriteMover {

    private float accelFactX = 0.0F;
    private float accelFactY = 500.0F;
    private float damp = 0.0F;
    private Random rand = new Random();
    private final float yEquilibrium;
    private final float mod;
    private final float phase;
    private final float amp;
    private  float time;

    TargetSpriteMover(float yEqu, float amp, float mod, float phase) {
        super();
        this.yEquilibrium = yEqu;
        this.mod = mod;
        this.phase = phase;
        this.amp = amp;
        this.time=0.0f;
    }

    TargetSpriteMover(float yEqu) {
        this(yEqu, 0, 0, 0);
    }

    public void move(MySprite s, float dt) {
        s.x = s.x + s.dxdt * dt;
        time+=dt;
        s.dxdt = s.dxdt + accelFactX * (rand.nextFloat() - 0.5F) * dt;
        if (s.dead) {
            s.y = s.y + s.dydt * dt;
            s.dydt = s.dydt + accelFactY * dt;
        } else {
            s.y = s.initY+(float) (amp * Math.cos(time * mod + phase));
        }
    }

    public float getbase() {
        return yEquilibrium;
    }
}
