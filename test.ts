/** Test class C */
export interface C {
  a: number;
  b: number[];
}

/** Test class B */
export interface B {
  e: any;
  f: C;
}

/** Test class A */
export interface RootData {
  a: number;
  b: B;
}

export interface State {
  root_data: RootData;
}
