%include global constraints
include "globals.mzn";

%x is horizontal, y is vertical
%w is horizontal, and it's fixed
%l is the minimum length we want to find, it's vertical (height of the plate)

%parameters
int: w;
int: n;
set of int: N = 1..n;
array [1..n, 1..2] of int: silicons;

int: maxlen = sum(i in N, j in 1..2)(silicons[i,j]);%maximum possible length, sum of all the heights of the single silicons
int: minlen = (sum(i in N)(silicons[i,2]*silicons[i,1]))div w;

var minlen..maxlen : l;

array [N] of var 0..1: rotation; %to know if the silicon is rotated or not 0=not rotated 10=rotated
array [N, 1..2] of var 0..maxlen:sizes;  %sizes is just like silicons, but instead of being all in one orientation, they can (or cannot) be flipped
array [N, 1..2] of var 0..maxlen:solution;

%constraint to make sure that the silicons are either in one orientation or the other
constraint forall(s in N)( 
    ((sizes[s,1] = silicons[s,1]) /\ (sizes[s,2] = silicons[s,2]) /* /\ (rotation[s]=0)*/) \/ 
    ((sizes[s,1] = silicons[s,2]) /\ (sizes[s,2] = silicons[s,1]) /* /\ (rotation[s]=1)*/)
);

constraint forall(s in N)( 
    ((sizes[s,1] = silicons[s,1]) /\ (rotation[s]=0)) \/
    ((sizes[s,1] = silicons[s,2]) /\ (rotation[s]=1))
    );

%get an array of the indexes ordered by height of the rectangle, because the taller the silicon, the more important the placement 
array[int] of int: order = sort_by(N, [-silicons[s,2]*silicons[s,1] | s in N]);   % try with area perimeter excetera, with area it's faster


%constraints
%ensuring that the silicones are within the width
constraint forall(s in N)(
    solution[s,1] + sizes[s,1] <= w
);

%constraint that sets the length
%the length must be greater equal than each one of the silicons' legth+yposition
constraint forall(s in N)(
   sizes[s,2] + solution[s,2] <= l
);

constraint
    diffn(
        [solution[s,1] | s in N],
        [solution[s,2] | s in N],
        [sizes[s,1] | s in N],
        [sizes[s,2] | s in N]
    );
    
%% ensure no overlap of silicons
constraint cumulative([solution[s,1] | s in N], [sizes[s,1] | s in N], [sizes[s,2] | s in N], l);
constraint cumulative([solution[s,2] | s in N], [sizes[s,2] | s in N], [sizes[s,1] | s in N], w);
    
%WITH ROTATION THIS ONE MAKES IT WORK
%TO TEST ON THE NON ROTATION FILE
constraint forall(s1,s2 in N where s1<s2)(
    (solution[s1,1] != solution[s2,1]) \/ (solution[s1,2] != solution[s2,2])
);

%constraint making sure that there's no gaps between silicons
%makes it take sligthly less in the rotation
%EVALUATE
constraint forall(s1 in order)(
  member([0] ++ [solution[s2,1] + sizes[s2,1] | s2 in order where s2 != s1], solution[s1,1]) /\
  member([0] ++ [solution[s2,2] + sizes[s2,2] | s2 in order where s2 != s1], solution[s1,2])
);

%symmetry breaking between two rectangles of the same dimentions, so that only one of the two solutions is considered
%EVALUATE
constraint forall(s1,s2 in N where s1 > s2)(
   if(sizes[s1,1] = sizes[s2,1] /\ sizes[s1,2] = sizes[s2,2]) then
     lex_less([solution[s1,1], solution[s1,2]] , [solution[s2,1], solution[s2,2]]) 
     else true endif
);

%if base is as long as w, lays it not rotated
constraint forall(s in N)(
  if(silicons[s,1] = w) then
    sizes[s,1] = silicons[s,1] /\ sizes[s,2] = silicons[s,2] /\ rotation[s] = 0
  else true endif
);

%if height is as long as w, lays it rotated
constraint forall(s in N)(
  if(silicons[s,2] = w) then
    sizes[s,1] = silicons[s,2] /\ sizes[s,2] = silicons[s,1] /\ rotation[s] = 1
  else true endif
);

%symmetry breaking? avoids rotating squares
constraint forall(s in N)(
  if(silicons[s,1] = silicons[s,2]) then
    rotation[s] = 0 /\ sizes[s,1] = silicons[s,1] /\ sizes[s,2] = silicons[s,2]
  else true endif
);


int: heur_type = 1;
int: seq_type = 1;
int: rest_type = 4;

ann: search_ann_l =
if heur_type == 1 then
  int_search([l], input_order, indomain_min, complete)
elseif heur_type == 2 then
  int_search([l], first_fail, indomain_min, complete)
elseif heur_type == 3 then
  int_search([l], dom_w_deg, indomain_min, complete)
elseif heur_type == 4 then
  int_search([l], input_order, indomain_random, complete)
elseif heur_type == 5 then
  int_search([l], first_fail, indomain_random, complete)
else
  int_search([l], dom_w_deg, indomain_random, complete)
endif;
  
ann: search_ann_s1 =
if heur_type == 1 then
  int_search([solution[s,1] | s in order], input_order, indomain_min, complete)
elseif heur_type == 2 then
  int_search([solution[s,1] | s in order], first_fail, indomain_min, complete)
elseif heur_type == 3 then
  int_search([solution[s,1] | s in order], dom_w_deg, indomain_min, complete)
elseif heur_type == 4 then
  int_search([solution[s,1] | s in order], input_order, indomain_random, complete)
elseif heur_type == 5 then
  int_search([solution[s,1] | s in order], first_fail, indomain_random, complete)
else
  int_search([solution[s,1] | s in order], dom_w_deg, indomain_random, complete)
endif;

ann: search_ann_s2 =
if heur_type == 1 then
  int_search([solution[s,2] | s in order], input_order, indomain_min, complete)
elseif heur_type == 2 then
  int_search([solution[s,2] | s in order], first_fail, indomain_min, complete)
elseif heur_type == 3 then
  int_search([solution[s,2] | s in order], dom_w_deg, indomain_min, complete)
elseif heur_type == 4 then
  int_search([solution[s,2] | s in order], input_order, indomain_random, complete)
elseif heur_type == 5 then
  int_search([solution[s,2] | s in order], first_fail, indomain_random, complete)
else
  int_search([solution[s,2] | s in order], dom_w_deg, indomain_random, complete)
endif;

ann: search_ann_seq = 
if seq_type == 1 then
  seq_search([search_ann_l, search_ann_s1,search_ann_s2])
elseif seq_type == 2 then
  seq_search([search_ann_l, search_ann_s2,search_ann_s1])
elseif seq_type == 3 then
  seq_search([search_ann_s1, search_ann_s2,search_ann_l])
elseif seq_type == 4 then
  seq_search([search_ann_s2, search_ann_s1,search_ann_l])
elseif seq_type == 5 then
  seq_search([search_ann_s1, search_ann_l,search_ann_s2]) 
else
  seq_search([search_ann_s2, search_ann_l,search_ann_s1]) 
endif;
  
ann: restart_ann =
if rest_type == 1 then
  restart_constant(100)
elseif rest_type == 2 then
  restart_linear(100)
elseif rest_type == 3 then
  restart_geometric(1.5, 100)
else restart_luby(100)
endif;
  

%output["\(silicons)"];
%solve minimize l;
%solve :: int_search(solution, input_order, indomain_min)  minimize l;

/*solve ::
 int_search([l], input_order, indomain_min, complete)
 :: seq_search([
 int_search([l], input_order, indomain_min, complete),
 int_search([solution[s,1] | s in order], input_order, indomain_min,complete),
 int_search([solution[s,2] | s in order], input_order, indomain_min,complete),
 ])
 minimize l;*/
 
solve:: search_ann_seq :: restart_ann minimize l;
 

 
 
 %we make sure that the two silicons don't overlap
%if we consider one silicon, we make sure that the other one is on the area adjacent to it
/*predicate my_no_overlap(var int:x1, var int:x2, var int:y1, var int:y2, var int:w1, var int:w2, var int:l1, var int:l2) =
  x1 + w1 <= x2\/
  y1 + l1 <= y2 \/
  x2 + w2 <= x1 \/
  y2 + l2 <= y1;
    
constraint forall(s1 in N)(
   forall(s2 in N where s1 < s2)(
     my_no_overlap(solution[s1,1], solution[s2,1], solution[s1,2], solution[s2,2], sizes[s1,1], sizes[s2,1], sizes[s1,2], sizes[s2,2])
));*/
