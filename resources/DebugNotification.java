package rx.plugins;

import rx.Notification;
import rx.Observable.OnSubscribe;
import rx.Observable.Operator;
import rx.Observer;
import rx.observers.SafeSubscriber;
import rx.operators.DebugSubscriber;

public class DebugNotification<T> {
    @Override
    public String toString() {
        final StringBuilder s = new StringBuilder("{");
        s.append(" \"nano\": ").append(nanoTime);
        s.append(", \"thread\": ").append(threadId);
        s.append(", \"observer\": \"").append(o.getClass().getName()).append("@").append(Integer.toHexString(o.hashCode())).append("\"");
        s.append(", \"type\": \"").append(kind).append("\"");
        if (notification != null) {
            if (notification.hasValue())
                s.append(", \"value\": \"").append(notification.getValue()).append("\"");
            if (notification.hasThrowable())
                s.append(", \"exception\": \"").append(notification.getThrowable().getMessage().replace("\\", "\\\\").replace("\"", "\\\"")).append("\"");
        }
        if (source != null)
            s.append(", \"source\": \"").append(source.getClass().getName()).append("@").append(Integer.toHexString(source.hashCode())).append("\"");
        if (from != null)
            s.append(", \"from\": \"").append(from.getClass().getName()).append("@").append(Integer.toHexString(from.hashCode())).append("\"");
        if (to != null)
            s.append(", \"to\": \"").append(to.getClass().getName()).append("@").append(Integer.toHexString(to.hashCode())).append("\"");
        s.append("}");
        return s.toString();
    }
}
