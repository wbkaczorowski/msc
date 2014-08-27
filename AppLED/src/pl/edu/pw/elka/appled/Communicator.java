package pl.edu.pw.elka.appled;

import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.Socket;

import android.os.AsyncTask;
import android.util.Log;

public class Communicator {
    
    public static final String TAG = "Communicator";
    
    public void sendData(String data) {
        new SendDataTask().execute(data);
      
    }
    
    //TODO pozmieniać to wszystko
    private class SendDataTask extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {
            String data = params[0];
            try {
                Socket socket = new Socket("192.168.1.14", 8234);
//                PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
//                out.write(data);
                BufferedOutputStream bos = new BufferedOutputStream(socket.getOutputStream());
                
                OutputStreamWriter osw = new OutputStreamWriter(bos, "US-ASCII");
         
                System.out.println("Sending message...");
         
                osw.write(data);
                osw.flush();
                
                Log.d(TAG, "Successfully sent " + data);
            } catch (IOException ioe) {
                Log.w(TAG, "takichuj " + ioe);
            }
            return null;
        }
        
    }

}
