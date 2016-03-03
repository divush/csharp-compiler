opt_rules = [ 'implicit_anonymous_function_parameter_list_opt',
	'generic_dimension_specifier_opt',
	'method_modifiers_opt',
	'variant_type_parameter_list_opt',
	'formal_parameter_list_opt',
	'get_accessor_declaration_opt',
	'indexer_modifiers_opt',
	'rank_specifiers_opt',
	'STMT_TERMINATOR_opt',
	'enum_member_declarations_opt',
	'for_initializer_opt',
	'constant_modifiers_opt',
	'set_accessor_declaration_opt',
	'enum_modifiers_opt',
	'enum_base_opt',
	'default_argument_opt',
	'array_initializer_opt',
	'struct_modifiers_opt',
	'accessor_modifier_opt',
	'switch_sections_opt',
	'namespace_member_declarations_opt',
	'explicit_anonymous_function_signature_opt',
	'property_modifiers_opt',
	'parameter_modifier_opt',
	'field_modifiers_opt',
	'variable_initializer_list_opt',
	'member_declarator_list_opt',
	'"partial"_opt',
	'class_base_opt',
	'explicit_anonymous_function_parameter_list_opt',
	'argument_name_opt',
	'type_parameter_constraints_clauses_opt',
	'statement_list_opt',
	'for_condition_opt',
	'struct_member_declarations_opt',
	'class_modifiers_opt',
	'expression_opt',
	'delegate_modifiers_opt',
	'for_iterator_opt',
	'object_or_collection_initializer_opt',
	'event_modifiers_opt',
	'dim_separators_opt',
	'constructor_initializer_opt',
	'member_initializer_list_opt',
	'using_directives_opt',
	'commas_opt',
	'class_member_declarations_opt',
	'constructor_modifiers_opt',
	'EXTERN_opt',
	'argument_list_opt' ]

#defining function to create _opt rules 
# def _create_empty_rule(opt_rules = []):
        # """ Given a rule name, creates an optional ply.yacc rule
            # for it. The name of the optional rule is
            # <rulename>_opt
        # """
for i in opt_rules :
        rulename = i[0:-4]
        print "def p_%s(p): \n \t \"\"\"%s : empty \n \t \t \t | %s\"\"\" \n" %(i, i, rulename)

