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

    }
}
