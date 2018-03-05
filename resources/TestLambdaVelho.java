package br.com.qualquer.coisa;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;

/*
 * Observações:
 */
public class TestLambdaVelho {

    private static final int TIMEOUT = 5;
    private static final String baseUrl = "http://localhost:8080";

    //TODO: Defina como true para executar testes
    private static final boolean ENABLED = false;

    @Test(dataProvider = "usuarios", enabled = ENABLED)
    public void test(Usuario usuario) {
        new Simulador(usuario);
    }
            private void goToDetalheUsuario() {
         
            waitUntil(TIMEOUT, new ExpectedCondition<Boolean>() {
                @Override
                public Boolean apply(WebDriver f) {
                    //String com comentário dentro 
                    String value = f.findElement(By.xpath("//*[@id=\"TESTE\"]/div[1]/h1/h1/h1/h1/h1")).getText();
                    return false;
                }
            });
        }

}
