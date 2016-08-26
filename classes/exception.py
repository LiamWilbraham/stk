import os

class MacroMolError(Exception):
    """
    A class for raising errors when using ``MacroMolecule`` instances.
    
    There are a lot of reason why MMEA might receive an error. The 
    error can originate when rkdit is trying to assembly a molucue, 
    sanitize it or manipulate it in some othe way. Equally, 
    optimizations may go wrong for one reason or another and raise an
    error. This is good, as problems should be identified, not ignored.
    
    However, errors raised just by rdkit are not as useful as one would
    hope. The error get raised but the user is not told which
    ``MacroMolecule`` instance was being manipulated. This makes
    replication of the error difficult as the GA randomly creates 
    molecules. For it to randomly replicate the error on the same 
    molecule is highly unlikely.
    
    In order to address this, whenever an error is raised by MMEA it
    should be placed into an error of this type. Error's of this class
    are initialized with the ``MacroMolecule`` instance that caused the
    error. Furthermore the ``MacroMolecule`` and rdkit/optimization/etc. 
    error is written to a file ``failures.txt``. This file is located in
    the same directory as the ``output`` direcotry. Writing the 
    ``MacroMolecule`` instance to file means it can be easily rebuilt as
    its building blocks, topology and any other parameters required for 
    initialization are written to this file. The writing happens during
    initialization of the error. This means that even if the error is
    ignored during runtime such as
        
        try:
            raise MacroMolError(...)
        
        except MacroMolError as ex:
            pass
        
    it will still be written to ``failures.txt`` and will not go
    undetected.
    
    Because of this, MMEA should always create error of this type when
    handling exception. This means every try/except statement in  MMEA
    should be something like:
    
        try:
            raise SomeExceptionByRdkit(...)
        
        except Exception as ex:
            MacroMolError(ex, macro_mol, 'error in init')
            
            # Do some stuff here. Reraise if you want or pass.
    
    This means that no error will go undected or ignored by accident.       
    
    Attributes
    ----------
    ex : Exception
        The exception raised by some other part of MMEA such as rdkit,
        or MacroModel.
        
    macro_mol : MacroMolecule
        The macromolecule on which the error was raised.
        
    notes : str
        Any additional comments about the exception. For example, where
        it is being raised.
    
    """
    
    def __init__(self, ex, macro_mol, notes):
        self.ex = ex
        self.macro_mol = macro_mol
        self.notes = notes
        self.write_to_file()
        print('MacroMolError written to ``failures.txt``.')
        
    def write_to_file(self):
        """
        Writes the exception and macromolecule to ``failures.txt``.
        
        This method is run during initialization. This means that even
        if an exception is ignored during runtime it will be still
        recorded in the ``failures.txt`` file.        
        
        """        
        
        cwd = os.getcwd()
        if os.name == 'nt':
            cwd = cwd.split('\\')
            cwd[0] += "\\"
        else:
            cwd = cwd.split('/')

        dir_ = []
        for x in cwd:
            if x == 'output' or x == 'MMEA':
                break
            dir_.append(x)

        dir_ = os.path.join(*dir_)
        name = os.path.join(dir_, 'failures.txt')

        try:
            with open(name, 'x') as f:
                pass
        except Exception as ex2:
            pass
        
        with open(name, 'a') as f:
            print(self.ex, file=f)
            print('note = ', self.notes, file=f)
            print('building blocks = ', self.macro_mol.building_blocks, file=f)
            print('topology = ', self.macro_mol.topology, file=f) 
            print('prist_mol_file = ', self.macro_mol.prist_mol_file, file=f) 
            print('topology_args = ', self.macro_mol.topology_args, file=f)
            print("\n\n\n", file=f)        