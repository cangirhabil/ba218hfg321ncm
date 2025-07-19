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

/* captcha_default_acp_demo.html */
class __TwigTemplate_27055ba5e1796ff3b5476a559ed1d00c extends \Twig\Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 1
        echo "<dl>
\t<dt><label for=\"captcha_preview\">";
        // line 2
        echo $this->extensions['phpbb\template\twig\extension']->lang("PREVIEW");
        echo $this->extensions['phpbb\template\twig\extension']->lang("COLON");
        echo "</label><br /><span>";
        echo $this->extensions['phpbb\template\twig\extension']->lang("CAPTCHA_PREVIEW_EXPLAIN");
        echo "</span></dt>
\t<dd><img src=\"";
        // line 3
        echo ($context["CONFIRM_IMAGE"] ?? null);
        echo "\" alt=\"";
        echo $this->extensions['phpbb\template\twig\extension']->lang("PREVIEW");
        echo "\" width=\"360\" height=\"96\" id=\"captcha_preview\" /></dd>
</dl>
";
    }

    public function getTemplateName()
    {
        return "captcha_default_acp_demo.html";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  47 => 3,  40 => 2,  37 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("", "captcha_default_acp_demo.html", "");
    }
}
