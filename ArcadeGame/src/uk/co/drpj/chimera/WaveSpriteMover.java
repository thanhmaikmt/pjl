package uk.co.drpj.chimera;

class WaveSpriteMover implements SpriteMover {

    float t = 0;
    private final float phase;
    private final float amp;
    private final float speed;
    private final float xAnchor;
    private final float yAnchor;
    ChimeraApp outer;

    WaveSpriteMover(float speed, float phase, float amp, float xAnchor, float yAnchor, ChimeraApp outer) {
        super();
        this.outer = outer;
        this.speed = speed;
        this.phase = phase;
        this.amp = amp;
        this.xAnchor = xAnchor;
        this.yAnchor = yAnchor;
    }

    public void move(MySprite s, float dt) {
        t += dt;
        s.x = (float) (xAnchor + Math.cos(t * speed + phase) * amp);
        s.y = (float) (yAnchor + Math.sin(t * speed + phase) * amp);
    }

    public float getbase() {
        throw new UnsupportedOperationException("Not supported yet.");
    }
}
