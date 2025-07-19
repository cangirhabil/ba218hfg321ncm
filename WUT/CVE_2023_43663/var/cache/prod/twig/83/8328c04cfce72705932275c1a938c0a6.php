<?php

use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Extension\SandboxExtension;
use Twig\Markup;
use Twig\Sandbox\SecurityError;
use Twig\Sandbox\SecurityNotAllowedTagError;
use Twig\Sandbox\SecurityNotAllowedFilterError;
use Twig\Sandbox\SecurityNotAllowedFunctionError;
use Twig\Source;
use Twig\Template;

/* @PrestaShop/Admin/Configure/AdvancedParameters/Employee/Blocks/form.html.twig */
class __TwigTemplate_e030a0302126c275b102866764272beb extends Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
            'employee_form' => [$this, 'block_employee_form'],
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 25
        echo "
";
        // line 26
        $this->env->getRuntime("Symfony\\Component\\Form\\FormRenderer")->setTheme(($context["employeeForm"] ?? null), [0 => "@PrestaShop/Admin/TwigTemplateForm/prestashop_ui_kit.html.twig"], true);
        // line 27
        $macros["ps"] = $this->macros["ps"] = $this->loadTemplate("@PrestaShop/Admin/macros.html.twig", "@PrestaShop/Admin/Configure/AdvancedParameters/Employee/Blocks/form.html.twig", 27)->unwrap();
        // line 29
        echo "
";
        // line 30
        $this->displayBlock('employee_form', $context, $blocks);
    }

    public function block_employee_form($context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 31
        echo "  ";
        echo         $this->env->getRuntime('Symfony\Component\Form\FormRenderer')->renderBlock(($context["employeeForm"] ?? null), 'form_start');
        echo "
  <div class=\"card\">
    <h3 class=\"card-header\">
      ";
        // line 34
        echo twig_escape_filter($this->env, $this->extensions['Symfony\Bridge\Twig\Extension\TranslationExtension']->trans("Employees", [], "Admin.Advparameters.Feature"), "html", null, true);
        echo "
    </h3>
    <div class=\"card-body\">
      <div class=\"form-wrapper\">
        ";
        // line 38
        echo $this->env->getRuntime('Symfony\Component\Form\FormRenderer')->searchAndRenderBlock(($context["employeeForm"] ?? null), 'widget');
        echo "
      </div>
    </div>
    <div class=\"card-footer\">
      <a href=\"";
        // line 42
        echo $this->extensions['Symfony\Bridge\Twig\Extension\RoutingExtension']->getPath("admin_employees_index");
        echo "\" class=\"btn btn-outline-secondary\" id=\"cancel-link\">
        ";
        // line 43
        echo twig_escape_filter($this->env, $this->extensions['Symfony\Bridge\Twig\Extension\TranslationExtension']->trans("Cancel", [], "Admin.Actions"), "html", null, true);
        echo "
      </a>
      <button class=\"btn btn-primary float-right\" id=\"save-button\">
        ";
        // line 46
        echo twig_escape_filter($this->env, $this->extensions['Symfony\Bridge\Twig\Extension\TranslationExtension']->trans("Save", [], "Admin.Actions"), "html", null, true);
        echo "
      </button>
    </div>
  </div>
  ";
        // line 50
        echo         $this->env->getRuntime('Symfony\Component\Form\FormRenderer')->renderBlock(($context["employeeForm"] ?? null), 'form_end');
        echo "

  ";
        // line 52
        $this->loadTemplate("@PrestaShop/Admin/Helpers/password_feedback.html.twig", "@PrestaShop/Admin/Configure/AdvancedParameters/Employee/Blocks/form.html.twig", 52)->display($context);
    }

    public function getTemplateName()
    {
        return "@PrestaShop/Admin/Configure/AdvancedParameters/Employee/Blocks/form.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  98 => 52,  93 => 50,  86 => 46,  80 => 43,  76 => 42,  69 => 38,  62 => 34,  55 => 31,  48 => 30,  45 => 29,  43 => 27,  41 => 26,  38 => 25,);
    }

    public function getSourceContext()
    {
        return new Source("", "@PrestaShop/Admin/Configure/AdvancedParameters/Employee/Blocks/form.html.twig", "/var/www/html/src/PrestaShopBundle/Resources/views/Admin/Configure/AdvancedParameters/Employee/Blocks/form.html.twig");
    }
}
