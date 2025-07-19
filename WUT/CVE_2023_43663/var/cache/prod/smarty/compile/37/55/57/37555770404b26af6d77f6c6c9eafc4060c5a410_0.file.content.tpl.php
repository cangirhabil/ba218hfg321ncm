<?php
/* Smarty version 4.3.1, created on 2025-05-13 08:26:56
  from '/var/www/html/admin589euclusrd3dvesrax/themes/default/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '4.3.1',
  'unifunc' => 'content_68233a90301791_90207288',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '37555770404b26af6d77f6c6c9eafc4060c5a410' => 
    array (
      0 => '/var/www/html/admin589euclusrd3dvesrax/themes/default/template/content.tpl',
      1 => 1689842302,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_68233a90301791_90207288 (Smarty_Internal_Template $_smarty_tpl) {
?><div id="ajax_confirmation" class="alert alert-success hide"></div>
<div id="ajaxBox" style="display:none"></div>
<div id="content-message-box"></div>

<?php if ((isset($_smarty_tpl->tpl_vars['content']->value))) {?>
	<?php echo $_smarty_tpl->tpl_vars['content']->value;?>

<?php }
}
}
