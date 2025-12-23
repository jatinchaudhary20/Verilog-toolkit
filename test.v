module full_adder (
  input a,
  input b,
  input cin, 
  output sum,
  output cout
);

  wire xor1, xor2; 

  xor (xor1, a, b);
  xor (sum, xor1, cin);

  and (and1, a, b);
  and (and2, cin, xor1);
  or (cout, and1, and2);

endmodule