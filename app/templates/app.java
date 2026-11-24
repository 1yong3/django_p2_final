Set<Interager> conjunto = new Hashset<Interager>();

conjunto.add(100);

if (conjunto.contains(100)){
    System.out.println("existe");
}
else{
    System.out.println("Não existe");
}

conjunto.add(100);

System.out.println(conjunto.stream().filter(n -> n==100).count());

// Resultado = 1 pois não permite repetição de valores