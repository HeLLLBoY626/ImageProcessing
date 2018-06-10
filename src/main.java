import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/* @author  Suman Paul
   @email   paulsuman@protonmail.com
 */
enum imgTyoe {
    P1,P2,P3,P4,P5,P6;
}
class consumer {

    consumer()
    {
        try(BufferedReader in=new BufferedReader(new FileReader("/home/suman/Pictures/image1.pgm")))
        {
            imgTyoe type=imgTyoe.valueOf(read(in));
            read(in);
            String line=read(in);
            int height= Integer.parseInt(line.substring(0,line.indexOf(' '))),width=Integer.parseInt(line.substring(line.indexOf(' ')+1));
            short[][] matrix=new short[height][width];
            for (int i = 0; i <(height*width) ; i++) {
                matrix[i/width][i%width]=Short.parseShort(read(in));
            }
            display(matrix);
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    void display(short[][] array)
    {
        for(short[] a:array)
        {
            for (short b:a)
                System.out.print(b+"\t");
            System.out.println();
        }
    }

    String read(BufferedReader in) throws IOException
    {
        String line=in.readLine().trim();
        return line.charAt(0)=='#' ? null:line ;
    }

    public static void main(String[] args) {
        new consumer();
    }
}
