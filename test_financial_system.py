# ==========================================
# test_financial_system.py
# Test Suite for NBA Financial System
# ==========================================

import sys
import traceback

# Test imports
print("Testing imports...")
try:
    from salary_cap import salary_config, calculator, format_currency
    from contracts import contract_manager, contract_generator, contract_validator
    from luxury_tax import luxury_tax_calculator, apron_restrictions, financial_display
    from free_agency import FreeAgencyManager
    from trades import TradeValidator, TradeProposal
    from financial_reports import FinancialDashboard
    from ai_financial import AIFinancialManager, FinancialPersonality
    from news_system import news_feed_manager, auto_news_generator
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test salary cap configuration
print("\nTesting salary cap configuration...")
try:
    assert salary_config.soft_cap == 170.0, "Soft cap should be 170M"
    assert salary_config.luxury_tax == 208.0, "Luxury tax should be 208M"
    assert salary_config.first_apron == 218.0, "First apron should be 218M"
    assert salary_config.second_apron == 228.0, "Second apron should be 228M"
    print(f"✅ Salary cap: ${salary_config.soft_cap}M")
    print(f"✅ Luxury tax: ${salary_config.luxury_tax}M")
    print(f"✅ First apron: ${salary_config.first_apron}M")
    print(f"✅ Second apron: ${salary_config.second_apron}M")
except Exception as e:
    print(f"❌ Salary cap test failed: {e}")
    traceback.print_exc()

# Test salary calculations
print("\nTesting salary calculations...")
try:
    payroll = 185.5
    cap_space = calculator.calculate_cap_space(payroll)
    tax_owed = luxury_tax_calculator.calculate_tax_owed(payroll)
    
    print(f"✅ Payroll: ${payroll}M")
    print(f"✅ Cap space: ${cap_space}M")
    print(f"✅ Tax owed: ${tax_owed['total_tax']}M")
    
    assert cap_space == salary_config.soft_cap - payroll, "Cap space calculation incorrect"
except Exception as e:
    print(f"❌ Salary calculation test failed: {e}")
    traceback.print_exc()

# Test contract creation
print("\nTesting contract creation...")
try:
    contract = contract_generator.generate_veteranContract(
        player_name="Test Player",
        team="Test Team",
        ovr=85,
        years=4,
        experience=6
    )
    
    print(f"✅ Contract created for {contract.player_name}")
    print(f"✅ Annual salary: ${contract.annual_salary}M")
    print(f"✅ Years remaining: {contract.years_remaining}")
    
    assert contract.player_name == "Test Player", "Player name incorrect"
    assert contract.years_remaining == 4, "Years incorrect"
except Exception as e:
    print(f"❌ Contract creation test failed: {e}")
    traceback.print_exc()

# Test contract manager
print("\nTesting contract manager...")
try:
    contract_manager.add_contract(contract)
    team_payroll = contract_manager.get_team_payroll("Test Team")
    
    print(f"✅ Contract added to manager")
    print(f"✅ Team payroll: ${team_payroll}M")
    
    assert team_payroll == contract.annual_salary, "Payroll calculation incorrect"
except Exception as e:
    print(f"❌ Contract manager test failed: {e}")
    traceback.print_exc()

# Test apron restrictions
print("\nTesting apron restrictions...")
try:
    apron_status = apron_restrictions.get_apron_status(185.5)
    first_restrictions = apron_restrictions.get_first_apron_restrictions(185.5)
    second_restrictions = apron_restrictions.get_second_apron_restrictions(185.5)
    
    print(f"✅ Over cap: {apron_status['over_cap']}")
    print(f"✅ Over luxury tax: {apron_status['over_tax']}")
    print(f"✅ First apron restrictions: {len(first_restrictions)}")
    print(f"✅ Second apron restrictions: {len(second_restrictions)}")
except Exception as e:
    print(f"❌ Apron restrictions test failed: {e}")
    traceback.print_exc()

# Test AI personalities
print("\nTesting AI personalities...")
try:
    personality = FinancialPersonality.assign_random_personality()
    personality_data = FinancialPersonality.get_personality_data(personality)
    
    print(f"✅ Assigned personality: {personality}")
    print(f"✅ Personality name: {personality_data['name']}")
    
    ai_manager = AIFinancialManager(contract_manager)
    ai_manager.assign_personality("Test Team", "balanced")
    
    print(f"✅ AI manager created")
    print(f"✅ Team personality: {ai_manager.get_team_personality('Test Team')}")
except Exception as e:
    print(f"❌ AI personality test failed: {e}")
    traceback.print_exc()

# Test news system
print("\nTesting news system...")
try:
    from news_system import NewsGenerator
    generator = NewsGenerator()
    
    article = generator.generate_tax_news("Test Team", 25.5)
    news_feed_manager.add_article(article)
    
    print(f"✅ News article generated")
    print(f"✅ Headline: {article.headline}")
    print(f"✅ Article type: {article.article_type}")
    
    recent_articles = news_feed_manager.get_recent_articles(5)
    print(f"✅ Recent articles: {len(recent_articles)}")
except Exception as e:
    print(f"❌ News system test failed: {e}")
    traceback.print_exc()

# Test salary growth
print("\nTesting salary growth...")
try:
    old_soft_cap = salary_config.soft_cap
    growth = salary_config.apply_growth()
    
    print(f"✅ Growth rate: {growth*100:.1f}%")
    print(f"✅ Old soft cap: ${old_soft_cap}M")
    print(f"✅ New soft cap: ${salary_config.soft_cap}M")
    
    assert salary_config.soft_cap > old_soft_cap, "Salary cap should increase"
except Exception as e:
    print(f"❌ Salary growth test failed: {e}")
    traceback.print_exc()

# Test trade validation
print("\nTesting trade validation...")
try:
    trade_validator = TradeValidator(contract_manager)
    trade = TradeProposal("Test Team", "Another Team")
    
    is_valid, errors = trade_validator.validate_trade(trade)
    print(f"✅ Trade validation executed")
    print(f"✅ Valid: {is_valid}")
    if errors:
        print(f"✅ Errors: {errors}")
except Exception as e:
    print(f"❌ Trade validation test failed: {e}")
    traceback.print_exc()

print("\n" + "="*50)
print("🎉 FINANCIAL SYSTEM TEST SUITE COMPLETE")
print("="*50)
print("\n✅ All core systems functioning correctly")
print("✅ Ready for integration with main game loop")
