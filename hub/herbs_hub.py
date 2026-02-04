from lib import g
from lib import components
from lib import sections

def main():
    url_slug = f'herbs'
    meta_title = 'Herbs – Complete Guide to Medicinal, Culinary & Healing Herbs'
    meta_description = 'Explore over 100,000 herbs, their benefits, uses, preparations, and related herbalism topics. Find herbs for stress, digestion, immunity, and more.'
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/herbs.html">'''
    import textwrap
    head_html = components.html_head(meta_title, meta_description, css='/styles-herb.css', canonical=canonical_html)

    intro_html = '''
<section id="intro">
  <h1 style="margin-bottom: 1.6rem;">Herbs: Medicinal Plants and Herbal Remedies</h1>
  <p>
    Herbs (<em>plants valued for therapeutic, culinary, and aromatic uses</em>) are plants or plant parts 
    that support wellness, flavor meals, and provide natural remedies. Unlike spices, which are often derived 
    from seeds, bark, or roots, herbs typically come from leaves, stems, or flowers. Herbs have been used for 
    thousands of years across traditional systems such as <a href="/herbalism.html">Ayurveda</a> 
    (e.g., <a href="/herbs/ashwagandha.html">Ashwagandha</a> / <em>Withania somnifera</em>), 
    <a href="/herbalism.html#tcm">Traditional Chinese Medicine</a> (e.g., <a href="/herbs/licorice.html">Licorice</a> / <em>Glycyrrhiza glabra</em>), 
    and European herbalism.
  </p>
  <p>
    This hub page serves as your comprehensive starting point to explore herbs for culinary, medicinal, 
    aromatic, and wellness purposes. You will find detailed <a href="#categories">herb categories</a>, 
    <a href="#featured-herbs">featured herbs</a>, and a full alphabetical index of herbs in our 
    <a href="/herbs/all.html">herb directory</a>. Each herb page contains information about its uses, 
    preparation methods, active compounds, and safety considerations.
  </p>
  <p>
    Whether you are a beginner seeking easy-to-use herbs like <a href="/herbs/chamomile.html">Chamomile</a> 
    or an experienced herbalist exploring adaptogens such as <a href="/herbs/rhodiola.html">Rhodiola</a>, 
    this page will guide you through the world of herbalism, linking to detailed category hubs, preparation 
    guides, and safety resources.
  </p>
</section>
    '''

    history_html = f'''
<section id="history">
  <h2>History & Cultural Significance of Herbs</h2>
  <p>
    Herbs have been used for thousands of years across cultures for medicine, food, and spiritual practices. 
    In <a href="/herbalism.html#ayurveda">Ayurveda</a>, herbs such as <a href="/herbs/ashwagandha.html">Ashwagandha</a> 
    (<em>Withania somnifera</em>) and <a href="/herbs/turmeric.html">Turmeric</a> (<em>Curcuma longa</em>) 
    have long been valued for vitality, immunity, and balance. Traditional Chinese Medicine (TCM) emphasizes herbs 
    like <a href="/herbs/licorice.html">Licorice</a> (<em>Glycyrrhiza glabra</em>) and <a href="/herbs/ginseng.html">Ginseng</a> 
    (<em>Panax ginseng</em>) to harmonize the body’s energy and treat specific conditions. European herbalism 
    historically focused on local herbs for healing, culinary use, and aromatic remedies.
  </p>
  <p>
    Key historical texts, such as <em>De Materia Medica</em> by Dioscorides, medieval herbals, and ancient manuscripts, 
    preserved generations of herbal knowledge. These works influenced modern herbal medicine and continue to 
    inform research into plant-based therapies.
  </p>
  <p>
    Across cultures, herbs were not only medicinal but also symbolic, used in rituals, culinary traditions, 
    and daily life. Understanding this historical and cultural context helps modern herbalists appreciate 
    the significance of herbs beyond their therapeutic effects, providing insight into how they are used 
    safely and effectively today.
  </p>
  <p>
    For more on the principles of herbalism and modern applications, see our 
    <a href="/herbalism.html">Overview of Herbalism</a> page.
  </p>
</section>
    '''

    taxonomy_html = f'''
<section id="taxonomy">
  <h2>How Herbs Are Classified</h2>
  <p>
    Herbs can be classified in multiple ways depending on their primary use, therapeutic effects, preparation methods, 
    or botanical family. Understanding these classifications helps herbalists, enthusiasts, and beginners explore herbs 
    effectively for culinary, medicinal, aromatic, and wellness purposes.
  </p>
  <article>
    <h3>Classification by Use</h3>
    <p>
      Herbs are often grouped by their main applications:
    </p>
    <ul>
      <li><strong>Culinary herbs:</strong> Enhance flavor in food and beverages, e.g., <a href="/herbs/basil.html">Basil</a> (<em>Ocimum basilicum</em>), <a href="/herbs/thyme.html">Thyme</a> (<em>Thymus vulgaris</em>).</li>
      <li><strong>Medicinal herbs:</strong> Support health, immunity, and digestion, e.g., <a href="/herbs/ginger.html">Ginger</a> (<em>Zingiber officinale</em>), <a href="/herbs/echinacea.html">Echinacea</a> (<em>Echinacea purpurea</em>).</li>
      <li><strong>Aromatic herbs:</strong> Used in teas, essential oils, or perfumes, e.g., <a href="/herbs/lavender.html">Lavender</a> (<em>Lavandula angustifolia</em>).</li>
    </ul>
  </article>
  <article>
    <h3>Classification by Effect</h3>
    <p>
      Herbs can also be categorized by their physiological or therapeutic effects, allowing targeted use for wellness or treatment:
    </p>
    <ul>
      <li><a href="/herbs/adaptogenic-herbs.html">Adaptogens</a> – help the body manage stress and promote energy balance.</li>
      <li><a href="/herbs/digestive-herbs.html">Digestive herbs</a> – support gastrointestinal health, soothe discomfort, and aid nutrient absorption.</li>
      <li><a href="/herbs/nervine-herbs.html">Nervine herbs</a> – calm the nervous system and improve sleep quality.</li>
      <li><a href="/herbs/immune-herbs.html">Immune-supporting herbs</a> – enhance defense mechanisms and recovery.</li>
    </ul>
  </article>
  <article>
    <h3>Classification by Preparation</h3>
    <p>
      The way herbs are prepared affects their potency and applications. Common preparation methods include:
    </p>
    <ul>
      <li><strong>Teas & Infusions:</strong> Water-based extractions, gentle and easy to prepare.</li>
      <li><strong>Tinctures:</strong> Alcohol-based extracts for concentrated active compounds.</li>
      <li><strong>Oils & Salves:</strong> Infused oils or topical applications for skin or joint support.</li>
      <li><strong>Powders & Capsules:</strong> Dried herbs in convenient, standardized forms for ingestion.</li>
    </ul>
    <p>
      Each method extracts different compounds, making some herbs more effective in specific forms. 
      For more details, visit our <a href="/preparations.html">Herbal Preparations</a> hub.
    </p>
  </article>
  <article>
    <h3>Classification by Botanical Family</h3>
    <p>
      Herbs can also be grouped by botanical families, which share growth patterns, chemical compounds, and therapeutic properties:
    </p>
    <ul>
      <li><strong>Mint family (Lamiaceae):</strong> Aromatic culinary herbs like <a href="/herbs/peppermint.html">Peppermint</a> (<em>Mentha × piperita</em>) and <a href="/herbs/thyme.html">Thyme</a>.</li>
      <li><strong>Ginger family (Zingiberaceae):</strong> Digestive and medicinal herbs like <a href="/herbs/ginger.html">Ginger</a>.</li>
      <li><strong>Sunflower family (Asteraceae):</strong> Includes herbs like <a href="/herbs/echinacea.html">Echinacea</a> and <a href="/herbs/chamomile.html">Chamomile</a>.</li>
    </ul>
    <p>
      Recognizing botanical families helps predict potential benefits, understand herb relationships, and identify interactions.
      For a complete guide, see our <a href="/botanical-families.html">Botanical Families of Herbs</a> page.
    </p>
  </article>
</section>
    '''

    categories_html = f'''
<section id="categories">
  <h2>Explore Herb Categories</h2>
  <p>
    Herbs are organized into categories based on their primary effects, uses, and traditional applications. 
    Each category represents a focused area of herbal knowledge. Click a category to visit its dedicated hub 
    for a complete list of herbs and detailed profiles.
  </p>
  <article>
    <h3>Adaptogenic Herbs</h3>
    <p>
      Adaptogens help the body adapt to physical, mental, and emotional stress, supporting energy, resilience, 
      and overall balance. Common adaptogens include <a href="/herbs/ashwagandha.html">Ashwagandha</a> 
      (<em>Withania somnifera</em>) and <a href="/herbs/rhodiola.html">Rhodiola</a> (<em>Rhodiola rosea</em>).
    </p>
    <a href="/herbs/adaptogenic-herbs.html">Explore all adaptogenic herbs →</a>
  </article>
  <article>
    <h3>Digestive Herbs</h3>
    <p>
      Digestive herbs support gastrointestinal health, soothe discomfort, and aid nutrient absorption. 
      Popular examples include <a href="/herbs/ginger.html">Ginger</a> (<em>Zingiber officinale</em>) 
      and <a href="/herbs/peppermint.html">Peppermint</a> (<em>Mentha × piperita</em>).
    </p>
    <a href="/herbs/digestive-herbs.html">Explore all digestive herbs →</a>
  </article>
  <article>
    <h3>Culinary Herbs</h3>
    <p>
      Culinary herbs enhance flavor and provide nutritional benefits. Examples include <a href="/herbs/basil.html">Basil</a> 
      (<em>Ocimum basilicum</em>) and <a href="/herbs/thyme.html">Thyme</a> (<em>Thymus vulgaris</em>).
    </p>
    <a href="/herbs/culinary-herbs.html">Explore all culinary herbs →</a>
  </article>
  <article>
    <h3>Nervine Herbs</h3>
    <p>
      Nervine herbs promote relaxation, support nervous system health, and improve sleep quality. 
      Common nervines include <a href="/herbs/chamomile.html">Chamomile</a> (<em>Matricaria chamomilla</em>) 
      and <a href="/herbs/lavender.html">Lavender</a> (<em>Lavandula angustifolia</em>).
    </p>
    <a href="/herbs/nervine-herbs.html">Explore all nervine herbs →</a>
  </article>
  <article>
    <h3>Immune-Supporting Herbs</h3>
    <p>
      Herbs that strengthen the immune system help the body defend against infections and maintain wellness. 
      Examples include <a href="/herbs/echinacea.html">Echinacea</a> (<em>Echinacea purpurea</em>) 
      and <a href="/herbs/elderberry.html">Elderberry</a> (<em>Sambucus nigra</em>).
    </p>
    <a href="/herbs/immune-herbs.html">Explore all immune-supporting herbs →</a>
  </article>
<article>
  <h3>Anti-inflammatory Herbs</h3>
  <p>
    Anti-inflammatory herbs help reduce inflammation in the body, support joint and tissue health, 
    and may aid in recovery from physical stress. Common examples include 
    <a href="/herbs/turmeric.html">Turmeric</a> (<em>Curcuma longa</em>) and 
    <a href="/herbs/ginger.html">Ginger</a> (<em>Zingiber officinale</em>).
  </p>
  <a href="/herbs/anti-inflammatory-herbs.html">Explore all anti-inflammatory herbs →</a>
</article>
<article>
  <h3>Detoxifying Herbs</h3>
  <p>
    Detoxifying herbs support the body’s natural elimination of toxins, promote liver and kidney function, 
    and enhance overall wellness. Common examples include 
    <a href="/herbs/dandelion.html">Dandelion</a> (<em>Taraxacum officinale</em>) and 
    <a href="/herbs/milk-thistle.html">Milk Thistle</a> (<em>Silybum marianum</em>).
  </p>
  <a href="/herbs/detoxifying-herbs.html">Explore all detoxifying herbs →</a>
</article>
</section>
    '''

    mechanisms_html = f'''
<section id="mechanisms">
  <h2>How Herbs Work: Active Compounds & Mechanisms</h2>
  <p>
    Herbs contain active compounds such as alkaloids, flavonoids, terpenes, glycosides, and essential oils that influence 
    the body in diverse ways. These compounds contribute to herbs’ medicinal, aromatic, and culinary properties, 
    supporting health across multiple systems.
  </p>
  <article>
    <h3>Physiological Effects</h3>
    <p>
      Different herbs affect the body through specific physiological actions:
    </p>
    <ul>
      <li><a href="/herbs/adaptogenic-herbs.html">Adaptogens</a> (e.g., <a href="/herbs/ashwagandha.html">Ashwagandha</a>) – modulate stress response and support adrenal function.</li>
      <li><a href="/herbs/nervine-herbs.html">Nervines</a> (e.g., <a href="/herbs/chamomile.html">Chamomile</a>) – calm the nervous system and improve sleep quality.</li>
      <li><a href="/herbs/immune-herbs.html">Immune-supporting herbs</a> (e.g., <a href="/herbs/echinacea.html">Echinacea</a>) – enhance defense mechanisms and recovery.</li>
    </ul>
  </article>
  <article>
    <h3>Active Compounds and Examples</h3>
    <p>Here are representative herbs with their key active compounds and primary effects:</p>
    <ul>
      <li><strong>Ashwagandha (<em>Withania somnifera</em>):</strong> Withanolides – support stress adaptation, vitality, and energy balance.</li>
      <li><strong>Ginger (<em>Zingiber officinale</em>):</strong> Gingerols – support digestion, reduce inflammation, and promote circulation.</li>
      <li><strong>Chamomile (<em>Matricaria chamomilla</em>):</strong> Apigenin – promotes relaxation, calmness, and sleep quality.</li>
      <li><strong>Turmeric (<em>Curcuma longa</em>):</strong> Curcumin – anti-inflammatory and antioxidant effects, supports joint and systemic health.</li>
      <li><strong>Rhodiola (<em>Rhodiola rosea</em>):</strong> Rosavins and salidroside – enhance resilience to fatigue and stress, improve mental clarity.</li>
    </ul>
  </article>
  <article>
    <h3>Mechanisms of Action</h3>
    <p>
      Herbs influence the body through various mechanisms, including:
    </p>
    <ul>
      <li>Modulation of stress hormones and adrenal function</li>
      <li>Support for digestive enzyme activity and gut health</li>
      <li>Activation and regulation of the immune system</li>
      <li>Anti-inflammatory and antioxidant pathways</li>
      <li>Neurotransmitter modulation for relaxation and mental clarity</li>
    </ul>
    <p>
      Understanding these mechanisms helps practitioners and herbal enthusiasts select herbs for specific wellness goals.
    </p>
  </article>
  <p>
    For practical guidance on using herbs, see our <a href="/preparations.html">Herbal Preparations</a> section, 
    which covers teas, tinctures, oils, powders, and salves. You can also explore herbs by category for targeted benefits 
    in the <a href="#categories">Herb Categories</a> section.
  </p>
</section>
    '''

    preparations_html = f'''
<section id="preparations">
  <h2>How Herbs Are Prepared</h2>
  <p>
    The method of preparing herbs affects their potency, flavor, and therapeutic effect. Different preparations 
    extract specific compounds and suit different applications, from culinary use to medicinal treatments. 
    Understanding these methods helps you make the most of each herb.
  </p>
  <article>
    <h3>Teas & Infusions</h3>
    <p>
      Teas and infusions are water-based extractions, often made from leaves, flowers, or stems. They are gentle, 
      easy to prepare, and commonly used for daily wellness. Examples include <a href="/herbs/chamomile.html">Chamomile tea</a> 
      and <a href="/herbs/peppermint.html">Peppermint infusion</a>.
    </p>
  </article>
  <article>
    <h3>Tinctures</h3>
    <p>
      Tinctures are alcohol-based extracts that concentrate the active compounds of herbs. They are ideal for 
      adaptogens, nervines, or herbs that require precise dosing. Examples include <a href="/herbs/ashwagandha.html">Ashwagandha tincture</a> 
      and <a href="/herbs/rhodiola.html">Rhodiola tincture</a>. See our <a href="/preparations.html">Herbal Preparations</a> hub for step-by-step instructions.
    </p>
  </article>
  <article>
    <h3>Oils & Salves</h3>
    <p>
      Infused oils and salves are used for topical applications to support skin, joints, and localized wellness. 
      Common examples include <a href="/herbs/lavender.html">Lavender oil</a> and <a href="/herbs/calendula.html">Calendula salve</a>. 
      These preparations extract lipophilic compounds that water-based methods cannot.
    </p>
  </article>
  <article>
    <h3>Powders & Capsules</h3>
    <p>
      Dried herbs can be ground into powders and encapsulated for convenient ingestion. This method preserves 
      active compounds and allows for standardized dosing. Examples include <a href="/herbs/turmeric.html">Turmeric powder</a> 
      and <a href="/herbs/ginger.html">Ginger capsules</a>.
    </p>
  </article>
  <p>
    Proper preparation ensures maximum benefits and safe use. For detailed instructions, recipes, and dosage 
    guidelines, see our <a href="/preparations.html">Herbal Preparations</a> hub, which covers teas, tinctures, oils, 
    powders, salves, and more.
  </p>
</section>
    '''

    synergy_html = f'''
<section id="synergy">
  <h2>Combining Herbs: Synergy & Blends</h2>
  <p>
    Herbs often work more effectively when combined, creating synergistic effects that enhance their therapeutic 
    or culinary benefits. Understanding common combinations helps you maximize wellness outcomes and create 
    balanced herbal blends.
  </p>
  <article>
    <h3>Stress and Adaptation Blends</h3>
    <p>
      Combining adaptogens can enhance stress resilience and energy balance. Examples include:
    </p>
    <ul>
      <li><a href="/herbs/ashwagandha.html">Ashwagandha</a> + <a href="/herbs/rhodiola.html">Rhodiola</a> – supports mental clarity, stress adaptation, and stamina.</li>
      <li><a href="/herbs/licorice.html">Licorice</a> + <a href="/herbs/eleuthero.html">Eleuthero</a> – supports adrenal function and energy.</li>
    </ul>
  </article>
  <article>
    <h3>Digestive Comfort Blends</h3>
    <p>
      Herbs can be combined to soothe digestion and improve nutrient absorption:
    </p>
    <ul>
      <li><a href="/herbs/ginger.html">Ginger</a> + <a href="/herbs/peppermint.html">Peppermint</a> – reduces bloating and nausea.</li>
      <li><a href="/herbs/fennel.html">Fennel</a> + <a href="/herbs/chamomile.html">Chamomile</a> – promotes calm digestion and gut comfort.</li>
    </ul>
  </article>
  <article>
    <h3>Immune Support Blends</h3>
    <p>
      Combining immune-supporting herbs may strengthen the body’s defense mechanisms:
    </p>
    <ul>
      <li><a href="/herbs/echinacea.html">Echinacea</a> + <a href="/herbs/elderberry.html">Elderberry</a> – supports immune response and reduces the duration of infections.</li>
      <li><a href="/herbs/ginger.html">Ginger</a> + <a href="/herbs/turmeric.html">Turmeric</a> – provides anti-inflammatory and antioxidant support.</li>
    </ul>
  </article>
  <p>
    For more detailed recipes, preparation tips, and recommended dosages, explore our 
    <a href="/preparations.html">Herbal Preparations</a> hub. Combining herbs responsibly ensures safety, 
    maximizes benefits, and enhances the effectiveness of your herbal blends.
  </p>
</section>
    '''

    featured_html = f'''
<section id="featured-herbs">
  <h2>Featured Herbs</h2>
  <p>
    While there are hundreds of herbs with unique properties, some herbs are particularly significant due to 
    their widespread use, historical importance, or scientifically recognized benefits. Below are featured herbs 
    from different categories of herbalism.
  </p>
  <article>
    <h3>Ashwagandha (<em>Withania somnifera</em>)</h3>
    <p>
      An adaptogenic herb renowned for supporting stress management, energy, and overall vitality. 
      Commonly used in teas, powders, and tinctures.
    </p>
    <a href="/herbs/ashwagandha.html">Read more →</a>
  </article>
  <article>
    <h3>Rhodiola (<em>Rhodiola rosea</em>)</h3>
    <p>
      An adaptogen that enhances resilience to stress and fatigue, supporting mental clarity and physical stamina.
    </p>
    <a href="/herbs/rhodiola.html">Read more →</a>
  </article>
  <article>
    <h3>Ginger (<em>Zingiber officinale</em>)</h3>
    <p>
      A digestive and immune-supporting herb used to relieve nausea, improve digestion, and reduce inflammation.
    </p>
    <a href="/herbs/ginger.html">Read more →</a>
  </article>
  <article>
    <h3>Chamomile (<em>Matricaria chamomilla</em>)</h3>
    <p>
      A calming nervine herb traditionally used to support relaxation, sleep, and digestive comfort.
    </p>
    <a href="/herbs/chamomile.html">Read more →</a>
  </article>
  <article>
    <h3>Turmeric (<em>Curcuma longa</em>)</h3>
    <p>
      Valued for its anti-inflammatory and antioxidant properties. Supports joint, liver, and overall systemic health.
    </p>
    <a href="/herbs/turmeric.html">Read more →</a>
  </article>
  <article>
    <h3>Peppermint (<em>Mentha × piperita</em>)</h3>
    <p>
      A digestive herb with aromatic properties. Supports gastrointestinal comfort and adds flavor to teas and dishes.
    </p>
    <a href="/herbs/peppermint.html">Read more →</a>
  </article>
  <article>
    <h3>Lavender (<em>Lavandula angustifolia</em>)</h3>
    <p>
      A nervine and aromatic herb used for relaxation, stress relief, and calming aromatherapy preparations.
    </p>
    <a href="/herbs/lavender.html">Read more →</a>
  </article>
  <article>
    <h3>Echinacea (<em>Echinacea purpurea</em>)</h3>
    <p>
      An immune-supporting herb commonly used to enhance the body's defense mechanisms and reduce the duration 
      of infections.
    </p>
    <a href="/herbs/echinacea.html">Read more →</a>
  </article>
</section>
    '''

    all_html = '''
<section id="all-herbs-preview">
  <h2>Complete List of Herbs</h2>
  <p>
    Explore our comprehensive directory of herbs. Below is a preview of some popular herbs, each linked to 
    its detailed page. You can browse the full alphabetical index to discover hundreds more, including their 
    uses, preparations, and health benefits.
  </p>
  <ul>
    <li><a href="/herbs/all.html#ashwagandha">Ashwagandha (<em>Withania somnifera</em>)</a></li>
    <li><a href="/herbs/all.html#ginger">Ginger (<em>Zingiber officinale</em>)</a></li>
    <li><a href="/herbs/all.html#rhodiola">Rhodiola (<em>Rhodiola rosea</em>)</a></li>
    <li><a href="/herbs/all.html#chamomile">Chamomile (<em>Matricaria chamomilla</em>)</a></li>
    <li><a href="/herbs/all.html#turmeric">Turmeric (<em>Curcuma longa</em>)</a></li>
    <li><a href="/herbs/all.html#eucalyptus">Eucalyptus (<em>Eucalyptus globulus</em>)</a></li>
    <li><a href="/herbs/all.html#peppermint">Peppermint (<em>Mentha × piperita</em>)</a></li>
    <li><a href="/herbs/all.html#lavender">Lavender (<em>Lavandula angustifolia</em>)</a></li>
    <li><a href="/herbs/all.html#licorice">Licorice (<em>Glycyrrhiza glabra</em>)</a></li>
    <li><a href="/herbs/all.html#lemon-balm">Lemon Balm (<em>Melissa officinalis</em>)</a></li>
  </ul>
  <p>
    <a href="/herbs/all.html">See the full herb index →</a>
  </p>
</section>
    '''

    faq_html = f'''
<section id="faq">
  <h2>Frequently Asked Questions About Herbs</h2>
  <article>
    <h3>What are herbs?</h3>
    <p>
      Herbs are plants or plant parts valued for their medicinal, culinary, aromatic, and therapeutic properties. 
      They differ from spices and supplements and are used across traditional and modern <a href="/herbalism.html">herbalism</a>. 
      For a complete list, see our <a href="/herbs/all.html">full herb index</a>.
    </p>
  </article>
  <article>
    <h3>How are herbs used in herbalism?</h3>
    <p>
      Herbs can be used in teas, tinctures, powders, oils, and salves. Their usage depends on the herb’s properties, 
      desired effect, and traditional practices. Learn more in our <a href="/preparations.html">Herbal Preparations</a> section.
    </p>
  </article>
  <article>
    <h3>Are herbs safe to use?</h3>
    <p>
      Most herbs are safe when used appropriately, but potency, interactions, and individual sensitivities matter. 
      Consult reliable sources or qualified herbalists for medicinal use. Some herbs are categorized by effects in hubs like 
      <a href="/herbs/adaptogenic-herbs.html">adaptogens</a> or <a href="/herbs/nervine-herbs.html">nervine herbs</a>.
    </p>
  </article>
  <article>
    <h3>How are herbs classified?</h3>
    <p>
      Herbs can be classified by use, effect, preparation, and botanical family. Understanding these classifications 
      helps select the right herb for culinary, medicinal, or aromatic purposes. See our <a href="#taxonomy">Classification section</a> for details.
    </p>
  </article>
  <article>
    <h3>Which herbs are best for beginners?</h3>
    <p>
      Beginner-friendly herbs are typically safe, easy to prepare, and widely used, such as <a href="/herbs/chamomile.html">Chamomile</a>, 
      <a href="/herbs/peppermint.html">Peppermint</a>, and <a href="/herbs/basil.html">Basil</a>. Starting with these allows you to explore herbal benefits safely.
    </p>
  </article>
  <article>
    <h3>How should herbs be stored?</h3>
    <p>
      Store herbs in cool, dry, and dark places to preserve potency. Dried herbs should be kept in airtight containers, 
      and fresh herbs can be refrigerated or frozen depending on the type. Proper storage ensures maximum benefits.
    </p>
  </article>
  <article>
    <h3>Where can I find a complete list of herbs?</h3>
    <p>
      Our full herb directory is available in the <a href="/herbs/all.html">complete herb index</a>, organized alphabetically 
      and by categories such as adaptogenic, digestive, and culinary herbs.
    </p>
  </article>
</section>
    '''

    related_html = f'''
<section id="related-hubs">
  <h2>Explore Related Topics</h2>
  <p>
    Herbs are part of a broader herbalism ecosystem. These related hubs provide additional information on 
    how herbs are prepared, applied, and integrated into wellness practices.
  </p>
  <ul>
    <li>
      <a href="/preparations.html">Herbal Preparations</a> – Learn about teas, tinctures, oils, salves, and other methods 
      of preparing herbs for maximum therapeutic or culinary benefit.
    </li>
    <li>
      <a href="/ailments.html">Herbs for Specific Conditions</a> – Discover which herbs are traditionally used for 
      digestive health, stress management, immunity, and more.
    </li>
    <li>
      <a href="/herbalism.html">Overview of Herbalism</a> – Explore the principles, history, and science behind herbal practices.
    </li>
    <li>
      <a href="/safety.html">Herb Safety and Guidelines</a> – Understand precautions, interactions, and proper usage 
      for safe herbal practices.
    </li>
    <li>
      <a href="/botanical-families.html">Botanical Families of Herbs</a> – Learn how herbs are grouped and the shared 
      characteristics within plant families.
    </li>
  </ul>
</section>
    '''

    safety_html = f'''
        <section id="safety">
          <h2>Herb Safety & Contraindications</h2>
          <p>
            While herbs offer many benefits, some can interact with medications, affect certain health conditions, 
            or be unsafe in high doses. Understanding precautions ensures safe and effective use.
          </p>
          <article>
            <h3>General Safety Guidelines</h3>
            <ul>
              <li>Consult a healthcare professional or qualified herbalist before using herbs for medicinal purposes.</li>
              <li>Start with small doses to assess tolerance and response.</li>
              <li>Follow recommended preparation and storage instructions to preserve potency.</li>
              <li>Avoid herbs known to cause allergies or adverse reactions if you have sensitivities.</li>
            </ul>
          </article>
          <article>
            <h3>Interactions with Medications</h3>
            <p>
              Some herbs can interact with prescription or over-the-counter medications, affecting their effectiveness 
              or causing side effects. Examples:
            </p>
            <ul>
              <li><a href="/herbs/ginger.html">Ginger</a> – may affect blood-thinning medications.</li>
              <li><a href="/herbs/ginseng.html">Ginseng</a> – can interact with diabetes or blood pressure medications.</li>
              <li><a href="/herbs/licorice.html">Licorice</a> – may influence blood pressure and potassium levels.</li>
            </ul>
          </article>
          <article>
            <h3>Special Populations</h3>
            <p>
              Certain herbs should be used with caution or avoided in specific populations:
            </p>
            <ul>
              <li>Pregnant or breastfeeding women – consult a professional before use.</li>
              <li>Children and elderly individuals – start with minimal doses and monitor effects.</li>
              <li>Individuals with chronic health conditions – some herbs may exacerbate symptoms or interact with treatments.</li>
            </ul>
          </article>
          <p>
            For more detailed guidelines, see our <a href="/safety.html">Herb Safety and Guidelines</a> hub, which provides 
            extensive information on safe usage, contraindications, and potential interactions.
          </p>
        </section>
    '''

    toc_html = '''
<nav id="table-of-contents" style="margin-bottom: 2rem;">
  <h2>Contents</h2>
  <ul>
    <li><a href="#intro">Introduction</a></li>
    <li><a href="#history">History & Cultural Significance</a></li>
    <li><a href="#taxonomy">How Herbs Are Classified</a></li>
    <li><a href="#categories">Explore Herb Categories</a></li>
    <li><a href="#mechanisms">How Herbs Work</a></li>
    <li><a href="#featured-herbs">Featured Herbs</a></li>
    <li><a href="#all-herbs-preview">Complete List of Herbs</a></li>
    <li><a href="#faq">Frequently Asked Questions</a></li>
    <li><a href="#related-hubs">Explore Related Topics</a></li>
  </ul>
</nav>
    '''


    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
          {sections.header()}
          <main class="container-md">
            {intro_html}
            {toc_html}
            {history_html}
            {taxonomy_html}
            {categories_html}
            {mechanisms_html}
            {preparations_html}
            {synergy_html}
            {featured_html}
            {all_html}
            {safety_html}
            {faq_html}
            {related_html}
          </main>
          {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)
    print(html)
    quit()

main()

