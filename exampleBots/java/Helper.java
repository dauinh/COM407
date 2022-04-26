//Evan Gray - May 2012
//Compile: javac Helper.java
//Run: java Helper
class Helper extends javaAI {
	int frames=0;
        @Override
        public void AI_loop() {
                frames++;
		if (frames==20) {
			thrust(1);
			frames=0;
		}
		else thrust(0);
		turnLeft(1);
		fireShot();
        }
        public Helper(String args[]) {
                super(args);
        }
        public static void main(String args[]) {
                String[] new_args = {"-name","Jelper"};
                Helper helper = new Helper(new_args);
        }
}
