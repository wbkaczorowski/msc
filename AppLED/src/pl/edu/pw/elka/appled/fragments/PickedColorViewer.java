package pl.edu.pw.elka.appled.fragments;

import pl.edu.pw.elka.appled.R;
import pl.edu.pw.elka.appled.Utils;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.view.View;

public class PickedColorViewer extends View {

    private Paint paint;
    private Rect rect;

    public PickedColorViewer(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init(context);
    }

    public PickedColorViewer(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }

    public PickedColorViewer(Context context) {
        super(context);
        init(context);
    }

    private void init(Context context) {
        rect = new Rect(0, 0, (int) Utils.convertDpToPixel(getResources().getDimension(R.dimen.picked_color_viever_size), context),
                (int) Utils.convertDpToPixel(getResources().getDimension(R.dimen.picked_color_viever_size), context));
    }

    public void updateColor(int color) {
        paint = new Paint();
        paint.setColor(color);
    }

    @Override
    public void onDraw(Canvas canvas) {
        canvas.drawRect(rect, paint);
    }
}