import java.time.LocalDate;
import java.util.HashSet;
import java.util.Objects;
 
interface Imprimivel {
    void imprimir();
}
 
class Aluno implements Imprimivel {
    private Integer id;
    private String nome;
 
    public Aluno(Integer id, String nome) {
        this.id = id;
        this.nome = nome;
    }
 
    public Integer getId() {
        return id;
    }
 
    public String getNome() {
        return nome;
    }
 
    @Override
    public void imprimir() {
        System.out.println("ID: " + id + " | Nome: " + nome);
    }
 
    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
 
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
 
        Aluno aluno = (Aluno) obj;
        return Objects.equals(id, aluno.id);
    }
 
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
 
class AlunoFormado extends Aluno {
    private LocalDate dataFormatura;
 
    public AlunoFormado(Integer id, String nome, LocalDate dataFormatura) {
        super(id, nome);
        this.dataFormatura = dataFormatura;
    }
 
    public LocalDate getDataFormatura() {
        return dataFormatura;
    }
 
    @Override
    public void imprimir() {
        System.out.println(
            "ID: " + getId() +
            " | Nome: " + getNome() +
            " | Data de Formatura: " + dataFormatura
        );
    }
}
 
public class Main {
    public static void main(String[] args) {
 
        HashSet<Aluno> alunos = new HashSet<>();
 
        Aluno aluno1 = new Aluno(1, "João");
        Aluno aluno2 = new Aluno(2, "Maria");
        Aluno aluno3 = new Aluno(3, "Carlos");
 
        AlunoFormado alunoFormado1 = new AlunoFormado(
            4,
            "Ana",
            LocalDate.of(2026, 7, 15)
        );
 
        AlunoFormado alunoFormado2 = new AlunoFormado(
            5,
            "Pedro",
            LocalDate.of(2026, 8, 20)
        );
 
        alunos.add(aluno1);
        alunos.add(aluno2);
        alunos.add(aluno3);
        alunos.add(alunoFormado1);
        alunos.add(alunoFormado2);
 
        System.out.println("===== ALUNOS CADASTRADOS =====");
 
        for (Aluno aluno : alunos) {
            aluno.imprimir();
        }
    }
}