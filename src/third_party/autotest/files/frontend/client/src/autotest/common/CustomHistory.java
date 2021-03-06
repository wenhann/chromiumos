package autotest.common;

import com.google.gwt.user.client.History;
import com.google.gwt.user.client.HistoryListener;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Wrapper around gwt.user.client.History that won't call onHistoryChanged for
 * programmatically-generated history items.
 *
 */
public class CustomHistory implements HistoryListener {
    private static final CustomHistory theInstance = new CustomHistory();
    
    public static class HistoryToken extends HashMap<String, String> {
        @Override
        public String toString() {
            return Utils.encodeUrlArguments(this);
        }
        
        public static HistoryToken fromString(String tokenString) {
            HistoryToken token = new HistoryToken();
            Utils.decodeUrlArguments(tokenString, token);
            return token;
        }
    }
    
    private List<CustomHistoryListener> listeners = new ArrayList<CustomHistoryListener>();
    private HistoryToken lastHistoryToken = new HistoryToken();
    
    public static interface CustomHistoryListener {
        public void onHistoryChanged(Map<String, String> arguments);
    }
    
    private CustomHistory() {
        History.addHistoryListener(this);
    }
    
    /**
     * Allows programmatic simulation of history changes, without actually changing history or the 
     * URL.
     */
    public static void simulateHistoryToken(HistoryToken token) {
        theInstance.onHistoryChanged(token.toString());
    }
    
    public static void processInitialToken() {
        theInstance.onHistoryChanged(History.getToken());
    }
    
    public void onHistoryChanged(String historyTokenString) {
        HistoryToken token;
        try {
            token = HistoryToken.fromString(historyTokenString);
        } catch (IllegalArgumentException exc) {
            return;
        }

        if (token.equals(lastHistoryToken)) {
            return;
        }

        lastHistoryToken = token;

        for (CustomHistoryListener listener : listeners) {
            listener.onHistoryChanged(token);
        }
    }
    
    public static HistoryToken getLastHistoryToken() {
        return theInstance.lastHistoryToken;
    }

    public static void addHistoryListener(CustomHistoryListener listener) {
        theInstance.listeners.add(listener);
    }
    
    public static void removeHistoryListener(CustomHistoryListener listener) {
        theInstance.listeners.remove(listener);
    }
    
    public static void newItem(HistoryToken token) {
        if (token.equals(getLastHistoryToken())) {
            return;
        }
        theInstance.lastHistoryToken = token;
        History.newItem(token.toString());
    }
}
