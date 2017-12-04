/*
*
* TESTE ABERTURA DE COMENTARIO
*
*
*/

package br.com.qualquer;

public class ClassDeclarationTest extends BaseGenericService<Long> implements InterfaceTest{

    private static final ClassDeclarationTest() {
    }

    private static final int MAXIMO = 5000;

    private static final String TEST_STRING = "teste_string";

    @PersistenceContext
    private EntityManager em;

    @Inject
    private Properties appProperties; //Teste comentário mesma linha da declaracao

    /**
     * Faz alguma coisa
     */
    public List<Long> findAll(String id) {
        return em.createNamedQuery("teste.buscaTodos", Long.class)
                .setParameter("id", id)
                .getResultList();
    }

    private static Classe fazAlgumaCoisa(Classe classe) {
        return MoreObjects.firstNonNull(Arrays.asList());
    }

    @Override
    protected EntityManager getEntityManager() {
        // TESTE Dentro do método
        return em;
    }
}
